import argparse
import h5py
import zipfile
import os

def exportar_eventos(h5_file, txt_file):
    """
    Exporta los primeros n eventos (t, x, y, p) desde un archivo .h5 a un .txt
    """
    with h5py.File(h5_file, "r") as f:
        images = f["images"]
        imagen = images[0]
        H, W = imagen.shape[:2]
    
        t = f["t"][:]
        x = f["x"][:]
        y = f["y"][:]
        p = f["p"][:]

    with open(txt_file, "w", encoding="utf-8") as out:
        out.write(f"{W} {H}\n")
    
        for i in range(len(t)):
            out.write(f"{t[i]} {int(x[i])} {int(y[i])} {p[i]}\n")
            
            
def comprimir_zip(txt_file):
    """
    Comprime un archivo .txt en un .zip y devuelve el nombre del zip
    """
    zip_file = f"{os.path.splitext(txt_file)[0]}.zip"
    with zipfile.ZipFile(zip_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(txt_file, arcname=os.path.basename(txt_file))
        
    os.remove(txt_file)
    
    return zip_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Exporta eventos desde un archivo .h5 a un archivo .txt"
    )
    parser.add_argument("-f", "--h5_file", required=True, help="Ruta al archivo de entrada .h5")
    parser.add_argument("-o", "--output_name", help="Ruta al archivo de salida de texto .zip")

    args = parser.parse_args()
    
    txt_file = args.output_name if args.output_name else f"eventos_{args.h5_file[:-3]}.txt"

    exportar_eventos(args.h5_file, txt_file)
    print(f"Se guardaron los eventos en {txt_file}")
    
    zip_file = comprimir_zip(txt_file)
    print(f"Se creó el archivo comprimido: {zip_file}")