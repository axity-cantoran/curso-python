# Módulo 01: Entorno y herramientas

## Objetivo

Configurar un entorno de desarrollo Python 3.12 utilizando Poetry, herramientas de calidad de código y validaciones automáticas con Git.

## Herramientas utilizadas

- Python 3.12
- Poetry
- Black
- isort (Aviso)
- Ruff
- pre-commit
- Git

## Configuración realizada

- Se creó un ambiente virtual administrado por Poetry.
- El ambiente virtual se configura dentro del proyecto en `.venv`.
- Se configuraron Black, isort y Ruff en `pyproject.toml`.
- Se creó un repositorio Git local.
- Se configuraron hooks de pre-commit para Black y Ruff.
- Se corrigió el formato del código mediante Black.
- Se analizaron y corrigieron problemas mediante Ruff.

## Incidencia con isort

isort se instaló correctamente como dependencia de desarrollo y aparece registrado en Poetry.

Sin embargo, Windows bloqueó su ejecución debido a una política corporativa de Control de aplicaciones. El sistema mostró el siguiente mensaje:

> Una directiva de Control de aplicaciones bloqueó este archivo.

Por esta razón:

- isort no pudo ejecutarse individualmente.
- isort no se agregó temporalmente a los hooks de pre-commit.
- Su configuración se conservó en `pyproject.toml`.
- Ruff se utilizó provisionalmente para revisar las reglas relacionadas con la organización de imports.

Esta es una excepción local y temporal. Cuando el área de TI autorice la ejecución de isort, deberá verificarse nuevamente y considerarse su incorporación al flujo de pre-commit.

## Comandos principales

Verificar Python:

```cmd
poetry run python --version