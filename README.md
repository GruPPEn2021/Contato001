# Como usar os arquivos json para configuração

Os arquivos json deve seguir os seguinte formato:

    {
        "port": 1,
        "notes": [
            [102, 62, "C5"],
            [61, 21, "D5"],
            [20, -20, "F5"],
            [-21, -61, "G5"],
            [-62, -102, "A#5"]
        ]
    }

port: porta midi
notes: notas e intervalos
    [
        valor minino do intervalo, valor maximo do intervado, nota
    ]
    