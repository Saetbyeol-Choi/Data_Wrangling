import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import io
from tabulate import tabulate
import matplotlib.patheffects as patheffects
import seaborn as sns
import matplotlib.pyplot as plt
import mpld3
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Send a request to the website
url = "https://justcreative.com/best-tablets-for-students/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

############################################### Market Share ####################################################################
# Find all the elements that contain the tablet information
tablet_elements = soup.find_all('h3', {'class': 'ftwp-heading'})

# Extract the tablet name and link for each tablet, as well as the popularity
tablets = []
for tablet_element in tablet_elements:
    match = re.search(r'\d+\. <a href="(.+)" rel="noopener">(.+)</a>', str(tablet_element))
    if match:
        name = re.sub('<[^<]+?>', '', match.group(2))
        link = match.group(1)
        rating_element = tablet_element.find_next('div', {'class': 'aawp-product__rating'})
        popularity_text = rating_element.find_next('div', {'class': 'aawp-product__reviews'}).text.strip()
        popularity = int(re.sub(r'[^0-9,]', '', popularity_text).replace(',', ''))
        tablets.append({'rank': len(tablets) + 1, 'name': name, 'link': link, 'popularity': popularity})

# Create a dictionary to store the count of each brand
brand_counts = {}
for tablet in tablets:
    brand = tablet['name'].split(' ')[0]
    if brand in brand_counts:
        brand_counts[brand] += 1
    else:
        brand_counts[brand] = 1

# Convert the dictionary to a list of tuples for sorting
brand_counts_list = [(k, v) for k, v in brand_counts.items()]

# Sort the list by the count of tablets in descending order
brand_counts_list.sort(key=lambda x: x[1], reverse=True)

# Create a list of the top tablets
top_tablets = [tablet['name'] for tablet in tablets if tablet['name'].split(' ')[0] != 'unknown']

# Create a formatted table of the top tablets
table = '<table><thead><tr><th>Rank</th><th>Tablet Name</th><th>Link</th></tr></thead><tbody>'
for tablet in tablets:
    table += f'<tr><td>{tablet["rank"]}</td><td>{tablet["name"]}</td><td><a href="{tablet["link"]}">{tablet["link"]}</a></td></tr>'
table += '</tbody></table>'

# Set the font for the plot
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 14

# Set the figure resolution to 300 dpi and adjust size
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

# Set the color palette for the pie chart
colors = sns.color_palette("Set2", n_colors=len(brand_counts_list))

# Plot the pie chart and add a border
ax.set_prop_cycle('color', colors)
pie, _, labels = ax.pie([x[1] for x in brand_counts_list], labels=[f"{x[0]} ({x[1]:.1f}%)" for x in brand_counts_list],
                        autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                        textprops={'fontsize': 12})

# Add a legend
legend = ax.legend(loc='center left', bbox_to_anchor=(1.3, 0.5), title='Tablet Brands', fontsize=14, title_fontsize=16,
                   frameon=False, prop={'family': 'sans-serif', 'size': 14, 'weight': 'bold'})
legend.get_title().set_fontfamily('serif')
legend.set_title('Tablet Brands', prop={'family': 'serif', 'size': 16, 'weight': 'bold'})

# Set the title and add a shadow
ax.set_title("Distribution of Tablet Brands", fontsize=24, fontweight='bold', fontfamily='serif') # fontfamily='sans-serif')
title = ax.title

# Remove unnecessary plot elements
ax.grid(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add a light grey background color to the plot
ax.set_facecolor('#F1F1F1')

# Set the font size of the tick labels
ax.tick_params(axis='both', which='major', labelsize=12)

# Add a grid to the plot
ax.grid(linestyle='--', linewidth=0.5, axis='y', alpha=0.7)

# Adjust the spacing between the plot and the legend
plt.subplots_adjust(right=0.75)

# Add a shadow to the legend
legend.set_path_effects([patheffects.withSimplePatchShadow(offset=(1,-1), shadow_rgbFace='grey', alpha=0.5)])

# Write the table and plot to an HTML file
with open('tablet_top_list.html', 'w') as f:
    f.write('<!DOCTYPE html>\n')
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<meta charset="UTF-8">\n')
    f.write('<title>Top Tablets</title>\n')
    f.write('<style>\n')
    f.write('body {\n')
    f.write('font-family: Arial, sans-serif;\n')
    f.write('background-color: #f2f2f2;\n')
    f.write('text-align: center;\n')
    f.write('}\n')
    f.write('header {\n')
    f.write('background-color: #4CAF50;\n')
    f.write('padding: 20px;\n')
    f.write('}\n')
    f.write('h1 {\n')
    f.write('color: white;\n')
    f.write('font-size: 36px;\n')
    f.write('font-weight: bold;\n')
    f.write('}\n')
    f.write('table {\n')
    f.write('margin: auto;\n')
    f.write('border-collapse: collapse;\n')
    f.write('width: 80%;\n')
    f.write('}\n')
    f.write('th, td {\n')
    f.write('padding: 12px;\n')
    f.write('text-align: left;\n')
    f.write('border-bottom: 1px solid #ddd;\n')
    f.write('}\n')
    f.write('th {\n')
    f.write('background-color: #4CAF50;\n')
    f.write('color: white;\n')
    f.write('}\n')
    f.write('caption {\n')
    f.write('font-size: 24px;\n')
    f.write('font-weight: bold;\n')
    f.write('margin-bottom: 20px;\n')
    f.write('}\n')
    f.write('figure {\n')
    f.write('margin: auto;\n')
    f.write('width: 80%;\n')
    f.write('}\n')
    f.write('figcaption {\n')
    f.write('text-align: center;\n')
    f.write('font-size: 24px;\n')
    f.write('font-weight: bold;\n')
    f.write('margin-top: 20px;\n')
    f.write('}\n')
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<header>\n')
    f.write('<h1>Top Tablets</h1>\n')
    f.write('</header>\n')
    f.write('<table>\n')
    f.write('<caption>Tablet Brands and Ranking</caption>\n')
    f.write(table)
    f.write('</table>\n')
    f.write('<figure>\n')
    f.write('<img src="tablet_brands.png">\n')
    f.write('<figcaption>Brand Distribution of Top Tablets</figcaption>\n')
    f.write('</figure>\n')
    f.write('<footer>\n')
    f.write('<p>&copy; 2023 Top Tablets. All rights reserved.</p>\n')
    f.write('</div>\n')
    f.write('</main>\n')
    f.write('<footer>\n')
    f.write('<div class="container">\n')
    f.write('</div>\n')
    f.write('</footer>\n')
    f.write('</body>\n')
    f.write('</html>\n')

# Save the plot as an image file
fig.savefig('tablet_brands.png', dpi=150, bbox_inches='tight')


############################################### Price ####################################################################
# Find all the elements that contain the tablet information
tablet_elements = soup.find_all('h3', {'class': 'ftwp-heading'})

# Extract the tablet name and latest price (if available) for each tablet
data = []
for tablet in tablet_elements:
    # Extract the tablet name
    name_element = tablet.find('a')
    if name_element is not None:
        name = name_element.text.strip()
    else:
        name = 'unknown'

    # Extract the latest price (if available)
    price_element = tablet.find_next('span', {'class': 'aawp-product__price--current'})
    if price_element is not None:
        price = price_element.text.strip()
        # Remove any non-numeric characters from the price string
        price = re.sub('[^0-9\.]', '', price)
        if price == '' or price.lower() == 'unknown':
            price = 'Price not available'
        else:
            price = f'${price}'
    else:
        price = 'Price not available'

    # Add the tablet name and latest price to the data list
    if name != 'unknown':
        data.append([name, price])

headers = ['Tablet Name', 'Latest Price on Amazon']
table = tabulate(data, headers=headers, tablefmt='html')
table = table.replace('<table>', '<table style="border-collapse: collapse; width: 50%; font-family: Arial, sans-serif;">')
table = table.replace('<th>', '<th style="border: 1px solid #ddd; padding: 12px; background-color: #f2f2f2; text-align: center; font-weight: bold; font-size: 16px;">')
table = table.replace('<td>', '<td style="border: 1px solid #ddd; padding: 12px; text-align: center; font-size: 14px;">')
table = table.replace('<tr>', '<tr style="border: 1px solid #ddd;">')

#Create the scatter plot
fig, ax = plt.subplots(figsize=(12, 6))
prices = [float(re.sub('[^0-9.]', '', d[1])) for d in data if d[1] != 'Price not available']
names = [d[0] for d in data if d[1] != 'Price not available']
colors = ['#7EB8DA' if p >= 500 else '#FEE08B' for p in prices] # Set colors based on price range
ax.scatter(names, prices, s=300, c=colors, edgecolor='black', linewidth=1.5)
ax.axhline(y=500, color='#FF1744', linestyle='--', alpha=0.5, linewidth=2.5)
ax.set_title('Latest Prices on Amazon', fontsize=22, fontweight='bold', pad=15)
ax.set_xlabel('Tablet Name', fontsize=16, fontweight='bold', color='#404040')
ax.set_ylabel('Price (USD)', fontsize=16, fontweight='bold', color='#404040')
ax.tick_params(axis='both', labelsize=12, length=0, pad=10)
for i, v in enumerate(prices):
    ax.text(i, v + 10, f'${v:.2f}', ha='center', fontsize=12, fontweight='bold')
plt.xticks(rotation=45, ha='right')

#Add gridlines
ax.grid(axis='y', linestyle='--', alpha=0.8, linewidth=1.2)
ax.yaxis.grid(True, linestyle='--', alpha=0.8, linewidth=1.2)

#Add a legend
legend_elements = [
plt.Line2D([0], [0], marker='o', color='w', label='Price >= $500', markerfacecolor='#7EB8DA', markersize=10),
plt.Line2D([0], [0], marker='o', color='w', label='Price < $500', markerfacecolor='#FEE08B', markersize=10)
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=12, frameon=False)

#Customize plot background and borders
ax.set_facecolor('#F2F2F2')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#E0E0E0')
ax.spines['left'].set_color('#E0E0E0')
ax.yaxis.grid(True, linestyle='--', alpha=0.5)

#Increase space between subplots
fig.subplots_adjust(wspace=0.3)

# Save the plot and the table as an HTML file
output_file = 'tablet_price.html'
with io.open(output_file, 'w', encoding='utf8') as f:
    f.write('<html><head><style>table {border-collapse: collapse; width: 50%; margin: auto;}')
    f.write('th, td {text-align: center; padding: 8px; border: 1px solid #ddd;}')
    f.write('th {background-color: #f2f2f2;}</style></head><body>')
    f.write(f'<h1 style="text-align: center; font-weight:bold;">Tablets by the price</h1>')
    f.write('<div style="display: flex; flex-direction: row; justify-content: center;">')
    f.write('<div style="width: 50%;">')
    f.write(table)
    f.write('</div>')
    f.write('<div>')
    f.write('<img src="scatter_plot.png" alt="scatter plot" style="width: 80%;">')
    f.write('</div>')
    f.write('</div>')
    f.write('</body></html>')
    plt.savefig('scatter_plot.png', dpi=100, bbox_inches='tight')


############################################### Reviews ####################################################################
# Find all h3 tags with class="ftwp-heading"
tablet_headings = soup.find_all("h3", class_="ftwp-heading")

# Extract the tablet names, links, and popularity from the h3 tag text using regular expressions
tablets = []
for heading in tablet_headings:
    match = re.search(r'\d+\. <a href="(.+)" rel="noopener">(.+)</a>', str(heading))
    if match:
        name = re.sub('<[^<]+?>', '', match.group(2))
        link = match.group(1)
        rating_element = heading.find_next('div', {'class': 'aawp-product__rating'})
        popularity_text = rating_element.find_next('div', {'class': 'aawp-product__reviews'}).text.strip()
        popularity = int(re.sub(r'[^0-9,]', '', popularity_text).replace(',', ''))
        tablets.append({'name': name, 'link': link, 'popularity': popularity})

# Sort the tablets by popularity in descending order
tablets = sorted(tablets, key=lambda t: t['popularity'], reverse=True)

# Bar chart of tablet popularity based on number of reviews on Amazon
n_tablets = len(tablets)
popularity_data = [t['popularity'] for t in tablets]

# Create a figure and axis object for the plot
fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
cmap = plt.get_cmap("Blues")
colors = cmap(np.linspace(0.2, 1.0, n_tablets))

# Create a horizontal bar plot
ax.barh(np.arange(n_tablets), popularity_data, color=colors, height=0.8, edgecolor="grey")

# Add y-axis labels and set tick parameters
ax.set_yticks(np.arange(n_tablets))
ax.set_yticklabels([t['name'][:35] for t in tablets], fontsize=14)
ax.set_ylabel('Device', fontsize=16, fontfamily='serif', fontweight='bold', labelpad=10)
ax.tick_params(axis='y', length=5, pad=5)

# Add x-axis labels and gridlines
ax.set_xlabel('Number of Reviews', fontsize=16, fontfamily='serif', labelpad=10)
ax.xaxis.grid(True, linestyle='--', color='#c5c5c5', linewidth=0.5)

# Set plot title and facecolor
ax.set_title('Tablet Popularity', fontsize=24, fontfamily='serif', fontweight='bold', pad=20)
# ax.set_title('Tablet Popularity', fontsize=24, fontweight='bold', pad=20)
ax.set_facecolor('#f4f4f4')

# Remove spines and ticks on right and top borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Add annotations with the number of reviews for each tablet to the right of the bars
for i, v in enumerate(popularity_data):
    ax.text(v + 100, i, format(v, ',d'), color='black', fontweight='bold', fontsize=14, fontfamily='serif')

# Add a legend for the bar chart
ax.legend(['Number of Reviews'], loc='upper right', fontsize=14, frameon=False, bbox_to_anchor=(1.02, 1.0), borderaxespad=0)

# Set the tight layout and save the figure as a PNG image
fig.tight_layout()

#Save the figure as a PNG image with a white background
plt.savefig('bar_plot.png', dpi=120, bbox_inches='tight', facecolor='white')

# Create an HTML file with the bar chart and tablet information
with open('tablet_reviews.html', 'w') as f:
    # Write the HTML code for the bar chart image
    f.write('<h1 style="text-align: center; font-family: serif; font-weight: bold;">Tablet Popularity</h1>\n')
    f.write('<div style="display: flex; justify-content: center; margin-bottom: 30px;">\n')
    f.write('<img src="bar_plot.png" alt="bar chart" style="width: 50%;">\n')
    f.write('</div>\n')
    # Write a table with the tablet information
    f.write(
        '<table style="margin: 0 auto; width: 50%; font-family: serif; font-size: 14px; border-collapse: collapse; border: 1px solid #ddd;">\n')
    f.write('<thead style="background-color: #f4f4f4; font-weight: bold; text-align: center;">\n')
    f.write('<tr><td style="padding: 10px; border: 1px solid #ddd;">Rank</td><td style="padding: 10px; border: 1px solid #ddd;">Tablet Name</td><td style="padding: 10px; border: 1px solid #ddd;">Number of Amazon Reviews</td></tr>\n')
    f.write('</thead>\n')
    f.write('<tbody>\n')
    for i, tablet in enumerate(tablets):
        f.write(f'<tr style="background-color: {"#ffffff" if i % 2 == 0 else "#f9f9f9"};"><td style="padding: 10px; text-align: center; border: 1px solid #ddd;">{i + 1}</td><td style="padding: 10px; border: 1px solid #ddd;"><a href="{tablet["link"]}" style="color: #1e90ff; text-decoration: none;">{tablet["name"]}</a></td><td style="padding: 10px; text-align: center; border: 1px solid #ddd;">{tablet["popularity"]:,}</td></tr>\n')
    f.write('</tbody>\n')
    f.write('</table>\n')
    # Add a footer with any additional information
    f.write('<div style="margin-top: 30px; font-family: serif; font-size: 12px; text-align: center; color: #777777;">\n')
    f.write('<p>Data collected on October 18, 2022 from <a href="https://www.amazon.com">Amazon.com</a>.</p>\n')
    f.write('<p>Created by <a href="https://www.example.com">John Doe</a>.</p>\n')
    f.write('</div>')


############################################### Rating ####################################################################
# Find all the elements that contain the tablet information
tablet_elements = soup.find_all('h3', {'class': 'ftwp-heading'})

# Extract the tablet name, rating score and number of reviews for each tablet
print('Tablet ratings and reviews on Amazon:')
tablets = []
for tablet in tablet_elements:
    # Extract the tablet name
    name_element = tablet.find('a')
    if name_element is not None:
        name = name_element.text.strip()
    else:
        name = 'unknown'

    # Extract the rating score and number of reviews
    rating_element = tablet.find_next('div', {'class': 'aawp-product__rating'})
    if rating_element is not None:
        rating_score = rating_element.find('span')['style']
        rating_score = re.findall('\d+', rating_score)
        if rating_score:
            rating_score = float(rating_score[0]) / 20  # Convert to 5-star rating
        else:
            rating_score = None
        num_reviews = rating_element.find_next('div', {'class': 'aawp-product__reviews'}).text.strip()
        num_reviews = int(re.sub('[^0-9]+', '', num_reviews))
    else:
        rating_score = None
        num_reviews = None

    # Calculate the weighted rating score
    if name != 'unknown' and rating_score is not None:
        tablets.append({'name': name, 'rating_score': rating_score, 'num_reviews': num_reviews})

# Check if any tablets were found
if not tablets:
    print('No tablets found on the webpage.')
else:
    # Calculate the average rating score
    total_rating_score = sum(tablet['rating_score'] for tablet in tablets)
    average_rating_score = total_rating_score / len(tablets)

    # Calculate the total number of reviews
    total_num_reviews = sum(tablet['num_reviews'] for tablet in tablets)

    # Set the minimum number of reviews required to be listed
    m = 10

    # Calculate the weighted rating score for each tablet
    for tablet in tablets:
        v = tablet['num_reviews']
        R = tablet['rating_score']
        C = average_rating_score
        if v >= m:
            tablet['weighted_rating_score'] = ((v / (v + m)) * R) + ((m / (v + m)) * C) * (v / total_num_reviews)
        else:
            tablet['weighted_rating_score'] = None

    # Sort the tablets by the weighted rating score and number of reviews in descending order
    tablets = [t for t in tablets if t['weighted_rating_score'] is not None] # remove tablets with None value for weighted_rating_score
    tablets = sorted(tablets, key=lambda x: (x['weighted_rating_score'], x['num_reviews']), reverse=True)

    # Print the tablets with their weighted rating score, rating score, and number of reviews
    for tablet in tablets:
        print(f"{tablet['name']}: Weighted rating: {tablet['weighted_rating_score']:.2f}, Rating score: {tablet['rating_score']:.2f}, Number of reviews: {tablet['num_reviews']}")

# Set up the figure and axis objects
fig, ax = plt.subplots(figsize=(8, 10))

# Define the heatmap data and plot the heatmap
heatmap_data = np.array([[tablet['weighted_rating_score']] for tablet in tablets])
heatmap = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto', vmin=0, vmax=5, alpha=0.8)

# Remove x-axis ticks and add y-axis tick labels
ax.set_xticks([])
ax.set_yticks(np.arange(len(tablets)))
ax.set_yticklabels([tablet['name'] for tablet in tablets], fontsize=14, fontname='Arial')

# Add a title to the plot
ax.set_title('Weighted Rating for Tablets', fontsize=24, fontfamily='serif', fontweight='bold', pad=20)

# Add the weighted rating score values to the heatmap with a white background
for i in range(len(tablets)):
    for j in range(1):
        text = ax.text(j, i, f"{heatmap_data[i][j]:.2f}", ha="center", va="center", color="black", fontsize=14, fontname='Arial', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

# Add a border to the heatmap
for pos in ['top', 'bottom', 'right', 'left']:
    ax.spines[pos].set_edgecolor('#333333')
    ax.spines[pos].set_linewidth(1.5)

# Add gridlines to the plot
ax.grid(which='major', axis='both', linestyle='-', color='#dddddd', linewidth=1)

# Adjust the spacing between the heatmap and the y-axis tick labels
ax.tick_params(axis='y', which='major', pad=10)

# Add a colorbar with a descriptive title
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
cbar = ax.figure.colorbar(heatmap, cax=cax)
cbar.ax.set_ylabel('Weighted Rating Score (out of 5)', rotation=-90, va="bottom", fontsize=16, labelpad=20)
cbar.ax.tick_params(labelsize=14)

# Tighten the layout
plt.tight_layout()

# Save the plot as an HTML file
html = mpld3.fig_to_html(fig)
with open('tablet_rating.html', 'w') as f:
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<style>\n')
    f.write('table {\n')
    f.write('border-collapse: collapse;\n')
    f.write('width: 100%;\n')
    f.write('}\n')
    f.write('th, td {\n')
    f.write('border: 1px solid #ddd;\n')
    f.write('text-align: left;\n')
    f.write('padding: 12px;\n')
    f.write('}\n')
    f.write('th {\n')
    f.write('background-color: #f2f2f2;\n')
    f.write('color: #000;\n')
    f.write('}\n')
    f.write('td {\n')
    f.write('font-size: 14px;\n')
    f.write('}\n')
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<div style="display:flex;flex-direction:row;justify-content:center;align-items:center;">\n')
    f.write('<div style="padding-right:50px;">\n')
    f.write('<img src="heatmap_plot.png" alt="heatmap" style="padding-left: 50px;">')
    f.write('</div>\n')
    f.write('<div>\n')
    f.write('<table>\n')
    f.write('<thead>\n')
    f.write('<tr><th>Name</th><th>Rating Score</th><th>Number of Reviews</th></tr>\n')
    f.write('</thead>\n')
    f.write('<tbody>\n')
    for tablet in tablets:
        f.write(f"<tr><td>{tablet['name']}</td><td>{tablet['rating_score']:.2f}</td><td>{'{:,}'.format(tablet['num_reviews'])}</td></tr>\n")
    f.write('</tbody>\n')
    f.write('</table>\n')
    f.write('</div>\n')
    f.write('</div>\n')
    f.write('</body>\n')
    f.write('</html>\n')
    plt.savefig('heatmap_plot.png')


