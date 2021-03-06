import numpy as np
from skimage.feature import corner_harris, corner_peaks
from ImFEATbox.__helperCommands import conv2float

def HarrisF(I, plotflag=False, N_s=0, returnShape=False):
    """
     Input:     - I: A 2D image
                - plotflag: a flag to enable/disable visualization
                  Default: plotflag = false
                - N_s: number of points considered to be the strongest points.
                  Default: N_s = ceil(0.1*N) (N: number of detected corners)

     Output:    - Out: A (1x10) vector containing 10 metrics calculated based
                       on corner points detected with Harris-Stephens algorithm
    """
    #
    # ************************************************************************
    # Implemented for MRI feature extraction by the Department of Diagnostic
    # and Interventional Radiology, University Hospital of Tuebingen, Germany
    # and the Institute of Signal Processing and System Theory University of
    # Stuttgart, Germany. Last modified: November 2016
    #
    # This implementation is part of ImFEATbox, a toolbox for image feature
    # extraction and analysis. Available online at:
    # https://github.com/annikaliebgott/ImFEATbox
    #
    # Contact: annika.liebgott@iss.uni-stuttgart.de
    # ************************************************************************

    if returnShape:
        return (10,1)

    # convert image
    I = conv2float(I)

    if np.iscomplexobj(I):
        I = np.real(I)

    # calculation of corner points using Harris-Stephens algorithm
    threshold = 7e-3

    N_s = 0
    c = corner_peaks(corner_harris(I), min_distance=3, threshold_rel=threshold)


    ## extract features
    N = c.shape[0]

    if N_s == 0 or N_s > 0.5*N:
        N_s = int(np.ceil(0.1*N))

    c_s = corners = corner_peaks(corner_harris(I), min_distance=3, num_peaks=N_s, threshold_rel=threshold)



    # determine center  of gravity for all points
    x_gravity = np.sum(c[:,0]/float(N))
    y_gravity = np.sum(c[:,1]/float(N))

    # deterime center of gravity for the strongest points
    x_gravity_s = np.sum(c_s[:,0]/float(N_s))
    y_gravity_s = np.sum(c_s[:,1]/float(N_s))

    # display the results
    if plotflag:
        plt.scatter(c[:,1],c[:,0], color='blue', marker="+", s=50)
        plt.scatter(c_s[:,1],c_s[:,0], color='red', marker="+", s=100)
        plt.plot(x_gravity_s, y_gravity_s, color='green', marker="*", MarkerSize=30)
        plt.show()
        #scatter(c(:,1),c(:,2),'+')
        #scatter(c_s(:,1),c_s(:,2),'g+')
        #plot(x_gravity_s, y_gravity_s,'r*','MarkerSize',10)


    # density of corner points
    dens = N / float(I.size)

    #standard derivation
    std_x = np.std(c[:,0], ddof=1)
    std_y = np.std(c[:,1], ddof=1)
    std_x_s = np.std(c_s[:,0], ddof=1)
    std_y_s = np.std(c_s[:,1], ddof=1)


    ## return feature vector
    Out = np.array([N, x_gravity, y_gravity, x_gravity_s, y_gravity_s, dens,
        std_x, std_y, std_x_s, std_y_s])

    print(Out)
    print(Out.shape)

    return Out
