import unicodedata

def get_median_df_byLOCATIONNAME(feature, df):
    median_feature = df.groupby('barrio')[feature].median()
    df_median_feature = median_feature.reset_index()
    df_median_feature.columns = ['NOMBRE', f"{feature}"]
    df_median_feature_sorted = df_median_feature.sort_values(by=f"{feature}", ascending=False)    
    return df_median_feature_sorted

def eliminar_acentos(texto):
    if isinstance(texto, str):
        texto = unicodedata.normalize('NFKD', texto)
        texto = ''.join([c for c in texto if not unicodedata.combining(c)])
    return texto

def procesar_datos(gdf, df_flats):
    gdf['NOMBRE'] = gdf['NOMBRE'].str.lower().apply(eliminar_acentos)
    df_flats['barrio'] = df_flats['barrio'].str.lower().apply(eliminar_acentos)
    gdf = gdf.to_crs(epsg=4326)
    centroide = gdf.geometry.centroid
    latitud = centroide.y.mean()
    longitud = centroide.x.mean()
    return gdf, df_flats, latitud, longitud