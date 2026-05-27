
| Nombre | Formato | Tamaño | Compresión | Contenido |
| --- | --- | --- |  --- | --- |
| Header | Bytes | Fijo | Ninguna | Infromación esencial del archivo, como el magic number, versión de snipp, UUID, index_offset |
| Metadata | JSON | Variable | LZMA-9 | Información general del snippet (nombre, descripción, fecha de creación, fecha de modificación, si tiene comandos, si tiene choices, etc)
| File_Index | JSON | Variable | LZMA-9 | Mapa de contenidos del snippet |
| Choices | JSON | Variable | LZMA-9 | Información sobre las choices del snippet |
| Commands | JSON | Variable | LZMA-9 | Información y contenido de los comandos que podría ejecutar el snippet al desplegarse, con autorización del usuario |
| Hooks | JSON | Variable | LZMA-9 | Información sobre los valores reemplazables del snippet.
| Contents | Bytes | Variable | 7z-9 | Contenido neto del snippet, en formato 7z
| Index | JSON | Variable | LZMA-9 | Mapa ubicaciones (offset) de cada parte del archivo. |
| End_Of_Snippet | bytes | Fijo | Ninguna | Firma de bytes indicando el final del snippet