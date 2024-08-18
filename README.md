
# **Urban Routes Automation Testing**

## **Descripción del proyecto**

**Urban Routes Automation Testing** es un proyecto diseñado para automatizar y verificar el flujo completo de solicitud de taxis a través de una aplicación web. El proyecto utiliza **Selenium** para emular la interacción del usuario con la interfaz, cubriendo escenarios críticos como la configuración de la ruta, la selección de tarifas, la introducción de información de pago, y la solicitud de servicios adicionales.

## **Tecnologías y técnicas utilizadas**

- **Python**: Lenguaje de programación principal utilizado para desarrollar las pruebas automatizadas.
- **Selenium**: Herramienta de automatización utilizada para emular la interacción con la aplicación web.
- **Pytest**: Framework de pruebas utilizado para estructurar y ejecutar las pruebas.
- **ChromeDriver**: Driver de Selenium utilizado para controlar el navegador Google Chrome durante las pruebas.
- **JSON**: Utilizado para manejar y parsear los logs de la aplicación, específicamente para interceptar y utilizar el código de confirmación del teléfono.
- **README.SO**: Utilizado para realizar la edición del archivo README.



## **Instrucciones para Ejecutar las Pruebas**

### **Prerrequisitos**

1. **Python**: Asegúrate de tener Python instalado en tu máquina.
2. **Selenium**: Instala Selenium usando pip:
   ```bash
   pip install selenium
   ```
3. **ChromeDriver**: Descarga ChromeDriver compatible con tu versión de Google Chrome y agrégalo al PATH de tu sistema.
4. **Pytest**: Instala Pytest usando pip:
   ```bash
   pip install pytest
   ```

### **Ejecutar las Pruebas**

1. Clona el repositorio en tu máquina local:
   ```bash
   git clone <git clone git@github.com:username/qa-project-Urban-Routes-es.git>
   ```

2. Ejecuta las pruebas con Pytest:
   ```bash
   pytest main.py
   ```

   Esto iniciará el navegador, ejecutará los escenarios de prueba, y generará un informe en la consola.

### **Consideraciones**

- **Ambiente de pruebas**: Asegúrate de estar en un ambiente de pruebas o staging, ya que las pruebas automatizadas emularán transacciones reales como la solicitud de taxis y la adición de tarjetas de crédito.

