import geopandas as gpd
import matplotlib.pyplot as plt


zip_path = './data/Barrios.zip'

gdf = gpd.read_file(f"zip://{zip_path}")

# Mostrar los primeros registros
print(gdf.head())

# Graficar los límites de los barrios
gdf.plot(edgecolor="black", figsize=(10, 10))
plt.title("Límites de los barrios")
plt.show()