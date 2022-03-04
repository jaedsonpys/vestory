# Vestory - Fast, simple and practical

![BADGE](https://img.shields.io/static/v1?label=status&message=desenvolvimento&color=red&style=flat-square)
![BADGE](https://img.shields.io/static/v1?label=licença&message=GPL%20v3.0&color=red&style=flat-square)
![BADGE](https://img.shields.io/static/v1?label=linguagem&message=Python&color=orange&style=flat-square)
![BADGE](https://img.shields.io/static/v1?label=tipo&message=CLI&color=blue&style=flat-square)

**Vestory** (junção de "Version" e "History"), é um controle de versões prático e rápido usado em qualquer terminal por linha de comando (**CLI**). Com comandos simples e fáceis de lembrar, facilitando o uso.

O projeto tem o código-aberto com uso da licença GNU General Public License v3.0. [Leia a licença](#Licença)

### Links

- [Versão 1.2](#Versão-1.2)
- [Instalação](#Instalação)
- [Como funciona](#Como-funciona)
- [Utilizando o Vestory](#Utilizando-o-Vestory)
    - [Inicializando repositório](#Inicializando-repositório)
    - [Adicionar arquivos](#Adicionar-arquivos)
    - [Submeter alterações](#Submeter-alterações)
    - [Juntar alterações](#Juntar-alterações)
    - [Ver log de alterações](#Ver-log-de-alterações)
    - [Status dos arquivos](#Status-dos-arquivos)
    - [Ignorando arquivos ou diretórios](#Ignorando-arquivos-ou-diretórios)
- [Licença](#Licença)

## Versão 1.2

Esta versão do Vestory pode:

- [x] Monitorar alterações de arquivos;
- [x] Salvar alterações de arquivos;
- [x] Ver logs de alterações;
- [x] Juntar alterações do arquivo;
- [x] Ignorar arquivos;

## Instalação

Para instalar o **Vestory**, utilize o gerenciador de pacotes PyPi:

```
pip install vestory
```

Após isso, você poderá utilizá-lo pela linha de comando com o comando `vestory`.

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

### Juntar alterações

Com o argumento `join`, você irá juntar todas as alterações de um arquivo, substituindo o arquivo original. Veja o uso deste argumento:

```
vestory join
```
<!-- 
Este comando irá fazer com que todos os arquivos que estão sendo rastreados juntem suas alterações. Também é possível juntar as alterações de apenas um arquivo:

```
vestory join test.txt
``` -->

Observe que, aparecerá uma mensagem de aviso antes do processo ser realizado:

```
warning: the "join" command will replace the current files.
> Do you wish to proceed? [y/n] 
```

Confirmando, o processo será realizado.

### Ver log de alterações

Para ver todas as alterações que foram realizadas, utilize o argumento `log`:

```
vestory log
```

Será apresentado as seguintes informações:

- Nome do autor
- Email do autor
- Data da alteração
- ID da mudança
- Comentário sobre a alteração

### Status dos arquivos

O status do arquivo mostra se ele foi alterado ou não, para verificar essa informação, utilize o argumento `status`:

```
vestory status
```

### Ignorando arquivos ou diretórios

Para ignorar arquivos ou diretórios, crie um arquivo na raíz do seu diretório chamado `.ignoreme`. Adicione linha a linha cada arquivo/diretório que serão ignorados. Ao ignorar um arquivo, ele não será adicionado ao monitoramento de alterações quando utilizar o comando `add -a`, e nem terá suas alterações submetidas.

Na adição de subdiretórios em `.ignoreme`, faça isto desta forma:

```
dir/subdir
```

## Licença

GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.
