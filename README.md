# ds-tesis-ute
Bajar los datos desde el portal https://portal.ute.com.uy/precipitaciones-ocurridas-y-prevision-de-niveles

Los datos que se visualizan, son registrados en forma automática por los sensores de las estaciones remotas de la Red Hidrológica Telemétrica y puestos a disposición en tiempo real,
por lo que eventualmente y en forma temporal, podrían estar afectados por fallas ocurridas en los sensores automáticos. Por este motivo, al tratarse de información no controlada, UTE
no se hace responsable por el uso que se haga de la misma.


https://portal.ute.com.uy/sites/default/files/docs/Aportes%20Bonete%20hist%C3%B3rico%202019.pdf


https://portal.ute.com.uy/generacion-hidroelectrica-historico-mensual

https://sites.ute.com.uy/novedades/Lluvias/Internet_climerh.htm

https://internas.inumet.gub.uy/reportes/BoletinPluviometrico/R3_2020_12_08.png

# Run
```bash
python run.py
```

# Generate Requerimients
We used pipreqs

```bash
pip install pipreqs

# in the parent folder
pipreqs ds-tesis-ute
```


# Get Latitud and Longitud for Estaciones
Create the dataset download/MapaEstHid.csv 

```bash
python get_lat_lon_estaciones.py
```
# Create data with Latitud and Longitud for Estaciones
Create the dataset download/data_latlon.csv

```bash
python complete_lat_lon.py
```
# Generate data 
Create the dataset download/ute/csv/*.csv

```bash
python gen_estacion_latlon.py
```