const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

// Enable CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  next();
});

// Initialize directory structure
function initializeDirectoryStructure() {
  const sourceDir = path.join(__dirname, 'sg_food_images_3');
  const acceptedDir = path.join(__dirname, 'accepted');
  const quarantineDir = path.join(__dirname, 'quarantine');

  // Create base directories if they don't exist
  [acceptedDir, quarantineDir].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir);
    }
  });

  // Get all category folders from source
  const categories = fs.readdirSync(sourceDir)
    .filter(item => fs.statSync(path.join(sourceDir, item)).isDirectory());

  // Create matching category folders in accepted and quarantine
  categories.forEach(category => {
    [acceptedDir, quarantineDir].forEach(baseDir => {
      const categoryDir = path.join(baseDir, category);
      if (!fs.existsSync(categoryDir)) {
        fs.mkdirSync(categoryDir);
      }
    });
  });
}

// Initialize directories on server start
initializeDirectoryStructure();

// Get list of folders
app.get('/api/folders', (req, res) => {
  const imageDir = path.join(__dirname, 'sg_food_images_3');
  try {
    const folders = fs.readdirSync(imageDir)
      .filter(item => fs.statSync(path.join(imageDir, item)).isDirectory());
    res.json(folders);
  } catch (error) {
    res.status(500).json({ error: 'Error reading folders' });
  }
});

// Get images by status and folder
app.get('/api/images/:status/:folder?', (req, res) => {
  const { status, folder } = req.params;
  const imageDir = path.join(__dirname, 'sg_food_images_3');
  const acceptedDir = path.join(__dirname, 'accepted');
  const quarantineDir = path.join(__dirname, 'quarantine');

  function getAllFiles(dir) {
    let results = [];
    if (!fs.existsSync(dir)) return results;

    function traverse(currentDir, baseDir, relativePath = '') {
      if (!fs.existsSync(currentDir)) return;
      
      const items = fs.readdirSync(currentDir);
      
      items.forEach((item) => {
        const fullPath = path.join(currentDir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
          traverse(fullPath, baseDir, path.join(relativePath, item));
        } else {
          if (item.match(/\.(jpg|jpeg|png|gif)$/i)) {
            const folderName = relativePath.split(path.sep)[0] || '';
            results.push({
              name: item,
              path: fullPath.replace(__dirname, '').replace(/\\/g, '/'),
              relativePath: path.join(relativePath, item).replace(/\\/g, '/'),
              folder: folderName,
              category: folderName // Adding category for clarity
            });
          }
        }
      });
    }

    traverse(dir, dir);
    return results;
  }

  try {
    let images = [];
    const targetDir = status === 'pending' ? imageDir : 
                     status === 'accepted' ? acceptedDir : 
                     status === 'quarantine' ? quarantineDir : null;

    if (!targetDir) {
      return res.status(400).json({ error: 'Invalid status parameter' });
    }

    if (folder) {
      const folderPath = path.join(targetDir, folder);
      images = getAllFiles(folderPath);
    } else {
      images = getAllFiles(targetDir);
    }
    
    res.json(images);
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error reading directory' });
  }
});

// Serve images statically
app.use('/sg_food_images_3', express.static(path.join(__dirname, 'sg_food_images_3')));
app.use('/accepted', express.static(path.join(__dirname, 'accepted')));
app.use('/quarantine', express.static(path.join(__dirname, 'quarantine')));

// Handle image actions (accept/reject/undo)
app.post('/api/images/:action', (req, res) => {
  const { imagePath } = req.body;
  const { action } = req.params;
  
  try {
    const sourcePath = path.join(__dirname, imagePath);
    const fileName = path.basename(sourcePath);
    let category = '';

    // Extract the category from the path
    if (imagePath.includes('/sg_food_images_3/')) {
      category = imagePath.split('/sg_food_images_3/')[1].split('/')[0];
    } else if (imagePath.includes('/accepted/')) {
      category = imagePath.split('/accepted/')[1].split('/')[0];
    } else if (imagePath.includes('/quarantine/')) {
      category = imagePath.split('/quarantine/')[1].split('/')[0];
    }

    if (action === 'reject') {
      // Ensure category folder exists in quarantine
      const quarantineFolder = path.join(__dirname, 'quarantine', category);
      fs.mkdirSync(quarantineFolder, { recursive: true });
      
      // Copy file to quarantine with category structure
      const quarantinePath = path.join(quarantineFolder, fileName);
      fs.copyFileSync(sourcePath, quarantinePath);
      res.json({ message: 'Image moved to quarantine' });

    } else if (action === 'accept') {
      // Ensure category folder exists in accepted
      const acceptedFolder = path.join(__dirname, 'accepted', category);
      fs.mkdirSync(acceptedFolder, { recursive: true });
      
      // Copy file to accepted with category structure
      const acceptedPath = path.join(acceptedFolder, fileName);
      fs.copyFileSync(sourcePath, acceptedPath);
      res.json({ message: 'Image accepted' });

    } else if (action === 'undo') {
      // Remove file from accepted or quarantine
      if (fs.existsSync(sourcePath)) {
        fs.unlinkSync(sourcePath);
      }
      res.json({ message: 'Action undone successfully' });

    } else {
      res.status(400).json({ error: 'Invalid action' });
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Error processing image' });
  }
});

// Add reset endpoint before the PORT definition
app.post('/api/reset', (req, res) => {
  try {
    const acceptedDir = path.join(__dirname, 'accepted');
    const quarantineDir = path.join(__dirname, 'quarantine');

    function clearDirectory(dir) {
      if (!fs.existsSync(dir)) return;
      
      const items = fs.readdirSync(dir);
      for (const item of items) {
        const itemPath = path.join(dir, item);
        if (fs.statSync(itemPath).isDirectory()) {
          const files = fs.readdirSync(itemPath);
          for (const file of files) {
            try {
              const filePath = path.join(itemPath, file);
              if (fs.statSync(filePath).isFile()) {
                fs.unlinkSync(filePath);
                console.log(`Deleted file: ${filePath}`);
              }
            } catch (err) {
              console.error(`Error deleting file ${file}:`, err);
              // Continue with other files even if one fails
            }
          }
        }
      }
    }

    console.log('Starting reset operation...');
    console.log('Clearing accepted directory...');
    clearDirectory(acceptedDir);
    console.log('Clearing quarantine directory...');
    clearDirectory(quarantineDir);
    console.log('Reset operation completed.');

    // Always send a JSON response
    res.json({ success: true, message: 'Reset successful' });
  } catch (error) {
    console.error('Error during reset:', error);
    // Ensure error response is also JSON
    res.status(500).json({ 
      success: false, 
      error: error.message || 'Error during reset operation'
    });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
}); 