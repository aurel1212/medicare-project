import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def graph_3d(pca_vector, df):
    """
    Example
    -------
    ax1 = graph_3d(X_pca_transformed, test_df)
    ax.set_xlim(-5000000,20000000)
    ax.set_ylim(-1000000,8000000)
    ax.set_zlim(-3000000,3000000)
    plt.show()
    """

    xs = pca_vector[:,0]
    ys = pca_vector[:,1]
    zs = pca_vector[:,2]
    c = df['indicted']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.scatter(xs, ys, zs, c=c, alpha=.3)

    return ax