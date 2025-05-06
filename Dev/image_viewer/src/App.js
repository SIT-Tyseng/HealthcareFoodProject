import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardMedia,
  CardActions,
  Button,
  Typography,
  Box,
  Alert,
  Snackbar,
  Tabs,
  Tab,
  Paper,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Divider,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import BlockIcon from '@mui/icons-material/Block';
import UndoIcon from '@mui/icons-material/Undo';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

function TabPanel({ children, value, index }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`image-tabpanel-${index}`}
      aria-labelledby={`image-tab-${index}`}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function App() {
  const [images, setImages] = useState({
    pending: [],
    accepted: [],
    quarantine: []
  });
  const [folders, setFolders] = useState([]);
  const [selectedFolder, setSelectedFolder] = useState(null);
  const [notification, setNotification] = useState({ open: false, message: '', severity: 'success' });
  const [currentTab, setCurrentTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [resetDialogOpen, setResetDialogOpen] = useState(false);

  useEffect(() => {
    fetchFolders();
  }, []);

  useEffect(() => {
    if (selectedFolder !== null) {
      fetchAllImages();
    }
  }, [selectedFolder, currentTab]);

  const fetchFolders = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/folders');
      const data = await response.json();
      setFolders(data);
      if (data.length > 0 && selectedFolder === null) {
        setSelectedFolder(data[0]);
      }
    } catch (error) {
      showNotification('Error loading folders', 'error');
    }
  };

  const fetchAllImages = async () => {
    setLoading(true);
    try {
      const statuses = ['pending', 'accepted', 'quarantine'];
      const results = await Promise.all(
        statuses.map(status => fetchImages(status))
      );
      
      setImages({
        pending: results[0],
        accepted: results[1],
        quarantine: results[2]
      });
    } catch (error) {
      showNotification('Error loading images', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchImages = async (status) => {
    const url = selectedFolder
      ? `http://localhost:3001/api/images/${status}/${selectedFolder}`
      : `http://localhost:3001/api/images/${status}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Error fetching ${status} images`);
    }
    return response.json();
  };

  const handleAction = async (imagePath, action) => {
    try {
      // Optimistically update the UI state
      const imageCategory = imagePath.split('/')[2]; // Get category from path
      const updatedImages = { ...images };
      
      if (action === 'accept' || action === 'reject') {
        // Remove from pending and add to respective destination
        const imageToMove = updatedImages.pending.find(img => img.path === imagePath);
        if (imageToMove) {
          updatedImages.pending = updatedImages.pending.filter(img => img.path !== imagePath);
          if (action === 'accept') {
            updatedImages.accepted.push(imageToMove);
          } else {
            updatedImages.quarantine.push(imageToMove);
          }
        }
      } else if (action === 'undo') {
        // Check both accepted and quarantine arrays
        const fromAccepted = updatedImages.accepted.find(img => img.path === imagePath);
        const fromQuarantine = updatedImages.quarantine.find(img => img.path === imagePath);
        
        if (fromAccepted) {
          updatedImages.accepted = updatedImages.accepted.filter(img => img.path !== imagePath);
          // Create a new path for the pending image
          const pendingPath = imagePath.replace('/accepted/', '/sg_food_images_3/');
          updatedImages.pending.push({
            ...fromAccepted,
            path: pendingPath
          });
        } else if (fromQuarantine) {
          updatedImages.quarantine = updatedImages.quarantine.filter(img => img.path !== imagePath);
          // Create a new path for the pending image
          const pendingPath = imagePath.replace('/quarantine/', '/sg_food_images_3/');
          updatedImages.pending.push({
            ...fromQuarantine,
            path: pendingPath
          });
        }
      }

      // Update the state immediately
      setImages(updatedImages);

      // Make the server request
      const response = await fetch(`http://localhost:3001/api/images/${action}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imagePath }),
      });

      if (!response.ok) {
        throw new Error('Failed to process image');
        // If there's an error, we should ideally revert the optimistic update here
      }

      const actionMessages = {
        accept: 'Image accepted successfully',
        reject: 'Image moved to quarantine',
        undo: 'Image restored successfully'
      };

      showNotification(actionMessages[action] || 'Action completed', 'success');
    } catch (error) {
      showNotification(`Error processing image: ${error.message}`, 'error');
      // On error, refresh the images to ensure consistency with server state
      await fetchAllImages();
    }
  };

  const showNotification = (message, severity) => {
    setNotification({
      open: true,
      message,
      severity,
    });
  };

  const handleCloseNotification = () => {
    setNotification({ ...notification, open: false });
  };

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  const handleFolderSelect = (folder) => {
    setSelectedFolder(folder);
  };

  const handleReset = async () => {
    setLoading(true);
    let retries = 3;
    
    while (retries > 0) {
      try {
        const response = await fetch('http://localhost:3001/api/reset', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });

        const data = await response.json();
        
        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Reset failed');
        }

        // Clear accepted and quarantine arrays in the state
        setImages(prev => ({
          ...prev,
          accepted: [],
          quarantine: []
        }));

        // Fetch all images again to ensure state is in sync with server
        await fetchAllImages();

        showNotification('Reset successful - All images have been cleared', 'success');
        break; // Success, exit the retry loop
      } catch (error) {
        console.error('Reset error:', error);
        retries--;
        
        if (retries === 0) {
          showNotification(
            error.message === 'Failed to fetch' 
              ? 'Network error: Please check if the server is running (http://localhost:3001)'
              : error.message || 'Error during reset',
            'error'
          );
        } else {
          console.log(`Retrying... ${retries} attempts remaining`);
          await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second before retrying
        }
      }
    }
    
    setLoading(false);
    setResetDialogOpen(false);
  };

  const ImageGrid = ({ images, showActions = false, showUndo = false }) => (
    <Grid container spacing={3}>
      {images.length === 0 ? (
        <Grid item xs={12}>
          <Typography variant="body1" color="textSecondary" align="center">
            No images found in this category
          </Typography>
        </Grid>
      ) : (
        images.map((image, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
            <Card>
              <CardMedia
                component="img"
                height="200"
                image={`http://localhost:3001${image.path}`}
                alt={image.name}
                sx={{ objectFit: 'cover' }}
              />
              <Box p={1}>
                <Typography variant="body2" noWrap>
                  {image.name}
                </Typography>
                <Typography variant="caption" color="textSecondary" noWrap>
                  Folder: {image.folder || 'None'}
                </Typography>
              </Box>
              {showActions && (
                <CardActions sx={{ justifyContent: 'space-between', px: 2, pb: 2 }}>
                  <Button
                    variant="contained"
                    color="success"
                    startIcon={<CheckCircleIcon />}
                    onClick={() => handleAction(image.path, 'accept')}
                  >
                    Accept
                  </Button>
                  <Button
                    variant="contained"
                    color="error"
                    startIcon={<BlockIcon />}
                    onClick={() => handleAction(image.path, 'reject')}
                  >
                    Reject
                  </Button>
                </CardActions>
              )}
              {showUndo && (
                <CardActions sx={{ justifyContent: 'center', px: 2, pb: 2 }}>
                  <Button
                    variant="outlined"
                    startIcon={<UndoIcon />}
                    onClick={() => handleAction(image.path, 'undo')}
                  >
                    Undo
                  </Button>
                </CardActions>
              )}
            </Card>
          </Grid>
        ))
      )}
    </Grid>
  );

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography 
        variant="h4" 
        component="h1" 
        gutterBottom 
        align="center" 
        sx={{ mb: 4 }}
      >
        Image Review Interface
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={9}>
          <Paper sx={{ mb: 2 }}>
            <Tabs
              value={currentTab}
              onChange={handleTabChange}
              indicatorColor="primary"
              textColor="primary"
              variant="fullWidth"
              sx={{ minHeight: 0 }}
            >
              <Tab 
                label={`Interface (${images.pending.length})`} 
                sx={{ py: 1, minHeight: 0 }}
              />
              <Tab 
                label={`Accepted (${images.accepted.length})`} 
                sx={{ py: 1, minHeight: 0 }}
              />
              <Tab 
                label={`Quarantine (${images.quarantine.length})`} 
                sx={{ py: 1, minHeight: 0 }}
              />
            </Tabs>
          </Paper>

          {selectedFolder && (
            <Typography 
              variant="h6" 
              sx={{ 
                mb: 2, 
                color: 'text.secondary',
                fontWeight: 500
              }}
            >
              Category: {selectedFolder.replace(/_/g, ' ')}
            </Typography>
          )}

          {loading ? (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
              <CircularProgress />
            </Box>
          ) : (
            <>
              <TabPanel value={currentTab} index={0}>
                <ImageGrid images={images.pending} showActions={true} />
              </TabPanel>

              <TabPanel value={currentTab} index={1}>
                <ImageGrid images={images.accepted} showUndo={true} />
              </TabPanel>

              <TabPanel value={currentTab} index={2}>
                <ImageGrid images={images.quarantine} showUndo={true} />
              </TabPanel>
            </>
          )}
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ 
            position: 'sticky', 
            top: 20,
            maxHeight: 'calc(100vh - 40px)',
            display: 'flex',
            flexDirection: 'column'
          }}>
            <Typography variant="h6" sx={{ p: 1.5, bgcolor: 'primary.main', color: 'white' }}>
              Categories
            </Typography>
            <Divider />
            <List sx={{ 
              flexGrow: 1,
              overflow: 'auto',
              maxHeight: 'calc(100vh - 120px)'
            }}>
              {folders.map((folder) => (
                <ListItem key={folder} disablePadding>
                  <ListItemButton 
                    selected={selectedFolder === folder}
                    onClick={() => handleFolderSelect(folder)}
                    sx={{ py: 1 }}
                  >
                    <ListItemText 
                      primary={folder.replace(/_/g, ' ')}
                      primaryTypographyProps={{
                        fontSize: '0.9rem'
                      }}
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
            <Divider />
            <Box sx={{ p: 1.5 }}>
              <Button
                variant="contained"
                color="error"
                fullWidth
                startIcon={<RestartAltIcon />}
                onClick={() => setResetDialogOpen(true)}
              >
                Reset All
              </Button>
            </Box>
          </Paper>

          <Dialog
            open={resetDialogOpen}
            onClose={() => setResetDialogOpen(false)}
          >
            <DialogTitle>Confirm Reset</DialogTitle>
            <DialogContent>
              <DialogContentText>
                This will permanently delete all images from the Accepted and Quarantine folders. This action cannot be undone. Are you sure you want to continue?
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setResetDialogOpen(false)}>Cancel</Button>
              <Button 
                onClick={handleReset} 
                color="error" 
                variant="contained"
                startIcon={<RestartAltIcon />}
              >
                Reset
              </Button>
            </DialogActions>
          </Dialog>
        </Grid>
      </Grid>

      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={handleCloseNotification}
          severity={notification.severity}
          variant="filled"
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}

export default App; 