from BeautifulSoup import BeautifulSoup

def create_cluster_dictionary(df):
    fips = [str(x).zfill(5) for x in df_health_drop_null.index]
    cluster = df['predictions'].values
    cluster_dict = dict(zip(fips, cluster))

    return cluster_dict

def plot_county_cluster(filename='../data/USA_Counties_with_FIPS_and_names.svg', cluster_dict):
    # Load USA map
    svg_map = open(filename, 'r').read()
    # Load map into soup
    soup = BeautifulSoup(svg, selfClosingTags=['defs','sodipodi:namedview'])
    # Find counties
    paths = soup.findAll('path')
    # choose colors
    colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0"]

    # County style
    path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1\
    stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;\
    marker-start:none;stroke-linejoin:bevel;fill:'

    for p in paths:
        if p['id'] not in ["State_Lines", "separator"]:
            # pass
            try:
                cluster = cluster_dict[p['id']]
            except:
                continue
                 
            if cluster == 3:
                color_class = 3
            #elif cluster > 8:
            #    color_class = 4
            #elif cluster > 6:
            #    color_class = 3
            elif cluster == 2:
                color_class = 2
            elif cluster == 1:
                color_class = 1
            else:
                color_class = 0
     
            color = colors[color_class]
            p['style'] = path_style + color

    print soup.prettify()