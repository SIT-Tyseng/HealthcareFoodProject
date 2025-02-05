from torchvision import transforms
from torchvision.transforms import RandomAdjustSharpness, RandomAutocontrast, InterpolationMode

class identity:
    def __init__(self):
        self.compose = transforms.Compose([])

    def __call__(self, image):
        return self.compose(image)
        
class S0:
    def __init__(self, resize=238, centercrop=224):
        self.resize = resize
        self.centercrop = centercrop

        self.compose = transforms.Compose([
            transforms.Resize(
                self.resize, interpolation=InterpolationMode.BICUBIC),
            transforms.CenterCrop(self.centercrop),
            transforms.ToTensor(),
        ])
    
    def __call__(self, image):
        return self.compose(image)
    

class C2_1A:
    def __init__(self, angle=10):
        self.angle = angle
        self.compose = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.RandomVerticalFlip(),
            transforms.RandomRotation(self.angle)
        ])
    
    def __call__(self, image):
        return self.compose(image)
    
class C2_1B:
    def __init__(self, sharpness_factor=2, random_autocontrast=0.1):
        self.sharpness_factor = sharpness_factor
        self.random_autocontrast = random_autocontrast
        self.compose = transforms.Compose([
            RandomAdjustSharpness(sharpness_factor=self.sharpness_factor),
            RandomAutocontrast(p=self.random_autocontrast),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def __call__(self, image):
        return self.compose(image)
    
class D1:
    def __init__(self):
        self.compose = transforms.Compose([
            transforms.Normalize(mean=0.5, std=0.5)
        ])

    def __call__(self,image):
        return self.compose(image)
    
