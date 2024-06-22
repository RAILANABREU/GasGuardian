
# Gas Guardian - Trabalho APS

### Membros:
- Railan Gomes de Abreu (22201641)
- Igor Zimmer Gonçalves (22202682)
- Nicolas Lazzeri Pimenta (22203241)
- Joao Pedro Paixao de Matos Gubert (22203242)

## Bibliotecas Utilizadas
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- sqlite3

### Instalação
```bash
pip install customtkinter
sudo apt install python3-tk
pip install --upgrade Pillow
```

## Instruções de Uso

### Rodar a Tela do CRUD do Posto
```bash
python3 -m Raillan.telas.TelaPosto
```

### Rodar a Tela do CRUD do Tanque de Combustíveis
```bash
python3 -m telas.TelaTanqueCombustivel
```
ou
```bash
python3 -m Raillan.telas.TelaTanqueCombustivel
```

### Resolvendo Erros Comuns

#### Erro: `ModuleNotFoundError: No module named 'controladores'`

Caso apareça o erro:

```plaintext
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/Users/railanabreu/Documents/Projects/GasGuardian/Raillan/telas/TelaTanqueCombustivel.py", line 1, in <module>
    from controladores.controladorTanqueCombustivel import ControladorTanqueCombustivel
ModuleNotFoundError: No module named 'controladores'
```

Execute o seguinte comando para definir o caminho do projeto:
```bash
export PYTHONPATH=/caminho/para/o/projeto
```
Em seguida, execute novamente o comando para rodar a tela.

## Observações
- Usar Python 3.10 ou superior.
