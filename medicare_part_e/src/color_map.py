from BeautifulSoup import BeautifulSoup

def create_cluster_dictionary(df):
    """ 
    Creates dictionary with fips code as key and cluster assignment as value
    """
    fips = [str(x).zfill(5) for x in df_health_drop_null.index]
    cluster = df['predictions'].values
    cluster_dict = dict(zip(fips, cluster))

    return cluster_dict

def plot_county_cluster(filename, cluster_dict):
    """
    Takes SVG file of USA county map and colors accordingly
    """
    # Load USA map
    svg_map = open(filename, 'r').read()
    # Load map into soup
    soup = BeautifulSoup(svg_map, selfClosingTags=['defs','sodipodi:namedview'])
    # Find counties
    paths = soup.findAll('path')
    # choose colors
    #colors = ["#f5f5f5", "#e41a1c", "#377eb8", "#4daf4a", "#984ea3"] #grey, red, blue, green, purple: option 1
    colors = ["#f5f5f5", "#fc8d59", "#ffffbf", "#99d594"] #grey, orangeish, yellowish, light-green: option 2

    # County style
    path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1\
    stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;\
    marker-start:none;stroke-linejoin:bevel;fill:'
    # Recolors all states grey
    for p in paths:
        if p['id'] not in ["State_Lines", "separator"]:
            color = colors[0]
            p['style'] = path_style + color
    
    for p in paths:
        if p['id'] not in ["State_Lines", "separator"]:
            # pass
            try:
                cluster = cluster_dict[p['id']]
            except:
                #continue
                #colors = colors[0]
                #p['style'] = path_style + color
                continue
                
            if cluster == 1:
                color_class = 3
            elif cluster == 2:
                color_class = 1
            elif cluster == 0:
                color_class = 2
            else:
                color_class = 0
     
            color = colors[color_class]
            p['style'] = path_style + color

    return soup.prettify()