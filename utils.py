import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import numpy as np

from math import floor


class IndexTracker:
    def __init__(self, ax, X, vmin, vmax):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2
        self.vmin = vmin
        self.vmax = vmax

        self.im = ax.imshow(self.X[:, :, self.ind], vmax=self.vmax, vmin=self.vmin, cmap='gray') #cmap='gray',
        self.update()

    def on_scroll(self, event):
        # print("%s %s" % (event.button, event.step)) # print step and direction
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()

def interpolate_image(image_data, thickness, x_spacing, y_spacing, spacing):
    """
        Interpolates image_data arg to have spacing voxel dimensions, given the current ones i.e. thickness, x_spacing, y_spacing
    """
    # get pixel dim and compute new spatial dimensions
    x_resize = floor((image_data.shape[0] / (spacing[0] / x_spacing)))
    y_resize = floor((image_data.shape[1] / (spacing[1] / y_spacing)))
    z_resize = floor((image_data.shape[2] / (spacing[2] / thickness)))
    # create tensor
    tensor_i = torch.from_numpy(image_data).unsqueeze(0).unsqueeze(0).to(device='cuda')
    tensor_i = F.interpolate(tensor_i, size=(x_resize, y_resize, z_resize), mode='trilinear', align_corners=True)
    # get data back to cpu
    image_data = tensor_i.to(device="cpu").detach().cpu().numpy()
    image_data = np.squeeze(image_data)
    return image_data