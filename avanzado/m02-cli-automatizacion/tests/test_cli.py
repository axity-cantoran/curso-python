from typer.testing import CliRunner

from m02_cli_automatizacion.cli import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Gestiona órdenes" in result.stdout


def test_create_rejects_invalid_quantity() -> None:
    result = runner.invoke(
        app,
        [
            "create",
            "--product",
            "Teclado",
            "--quantity",
            "0",
            "--unit-price",
            "50",
        ],
    )

    assert result.exit_code != 0
