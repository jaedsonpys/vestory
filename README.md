# Vestory

![BADGE](https://img.shields.io/static/v1?label=status&message=desenvolvimento&color=red&style=flat)
![BADGE](https://img.shields.io/static/v1?label=versão&message=1.0.0&color=purple&style=flat)
![BADGE](https://img.shields.io/static/v1?label=linguagem&message=Python&color=orange&style=flat)
![BADGE](https://img.shields.io/static/v1?label=tipo&message=CLI&color=blue&style=flat)

**Vestory** (junção de "Version" e "History"), é um controle de versões prático e rápido usado em qualquer terminal por linha de comando (**CLI**). Com comandos simples e fáceis de lembrar, facilitando o uso.

O projeto tem o código-aberto com uso da licença GNU General Public License v3.0. [Leia a licença](#Licença)

### Links

- [Instalação](#Instalação)
- [Como funciona](#Como-funciona)
- [Utilizando o Vestory](#Utilizando-o-Vestory)
    - [Inicializando repositório](#Inicializando-repositório)
    - [Adicionar arquivos](#Adicionar-arquivos)
    - [Submeter alterações](#Submeter-alterações)
- [Licença](#Licença)

## Versão 1.0.0

Esta versão do Vestory possui:

- [x] Monitorar alterações de arquivos;
- [x] Salvar alterações de arquivos;
- [x] Ver logs de alterações;
- [x] Juntar alterações do arquivo.

Na próxima versão, será possível:

- [ ] Voltar na linha do tempo dos arquivos;
- [ ] Suporte a arquivos de: fotos, vídeos, executáveis, etc;
- [ ] Ver a diferença de uma alteração.

## Instalação

Para instalar o **Vestory**, utilize o gerenciador de pacotes PyPi:

```
pip install vestory
```

Após isso, você poderá utilizá-lo pela linha de comando com o comando `vestory`.

## Como funciona

Ao incializar um repositório, o Vestory irá criar o arquivo de configuração `vestory.config.json` e um diretório chamado `changes`. Dentro desse diretório ficará todas as mudanças de seus arquivos.

Por exemplo, o arquivo `app.py` ficará salvo como um arquivo no diretório `changes`. Dentro desse arquivo, cada linha em **Base64** representa uma alteração no arquivo, se decodificarmos esse base64, obteremos um **JSON** com as informações dessa alteração.

## Utilizando o Vestory

Primeiro, veja a lista de comandos disponíveis até o momento:

- `init`: cria um novo repositório;
- `add [files]`: adiciona os arquivos ao monitoramento de alterações;
- `submit`: salva as alterações realizadas até o momento.

### Inicializando repositório

Para incializar um repositório, utilize o comando `init`:

```
vestory init
```

Antes disso, é necessário que suas configurações estejam feitas para incializar um repositório
corretamente.

### Adicionar arquivos

Para adicionar arquivos ao monitoramento de alterações:

```
vestory add example.txt
```

Também é possível adicionar vários arquivos de uma vez, escrevendo o nome de cada um ou utilizando a flag `-a`:

```
vestory add example.txt test.py project/app.py
```
```
vestory add -a
```

> a flag `-a` adiciona todos os arquivos presentes no diretório.

### Submeter alterações

Para submeter uma alteração, você precisa especificar os arquivos, ou submeter a alteração de todos os arquivos que foram adicionados utilizando a flag `-a`.

Também é necessário adicionar um comentário sobre aquela alteração, para isso, utilizamos a flag `-c`. Veja um exemplo:

```
vestory submit example.txt -c 'first changes'
```

Você pode submeter as alterações de todos os arquivos monitorados e adicionar um comentário utilizando a abreviação `-ac`:

```
vestory submit -ac 'first changes'
```

### Ver log de alterações

Para ver todas as alterações que foram realizadas, utilize o argumento `log`:

```
vestory log
```

Será apresentado as seguintes informações:

- Nome do autor
- Email do autor
- Data da alteração
- Hash MD5 da alteração
- Comentário sobre a alteração

### Status dos arquivos

O status do arquivo mostra se ele foi alterado ou não, para verificar essa informação, utilize o argumento `status`:

```
vestory status
```

## Licença

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
