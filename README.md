# Aplicación de Gestión Financiera Hogar

Esta aplicación te ayuda a mantener un registro de tus ingresos y gastos del hogar, guardando toda la información en un archivo Excel.

## Características

- Registro de ingresos y gastos
- Categorización de transacciones
- Visualización de datos en tiempo real
- Archivo Excel actualizado automáticamente
- Interfaz gráfica fácil de usar

## Requisitos

- Python 3.7 o superior
- Microsoft Excel (para abrir el archivo generado)
- Las siguientes bibliotecas de Python:
  - pandas
  - openpyxl

## Instalación

1. Instalar las dependencias:
```bash
pip install pandas openpyxl
```

2. Ejecutar la aplicación:
```bash
python finanzas.py
```

## Uso

1. Selecciona el tipo de transacción (Ingreso o Gasto)
2. Elige la categoría correspondiente
3. Ingresa el monto
4. Agrega una descripción
5. Haz clic en "Agregar Transacción"

Los datos se guardarán automáticamente en el archivo `finanzas_hogar.xlsx`
