# Proyecto de Sensor de Pinza Robótica

Este repositorio contiene proyectos de investigación robótica centrados en la detección táctil y la manipulación utilizando el entorno de simulación Isaac Lab.

## Estructura del Proyecto

- **`cabinet_sensor_project/`** - Proyecto principal que contiene la pinza Franka Panda con sensores de contacto integrados
- **`gripper_sensor_data/`** - Datos de sensores recopilados de los experimentos

## Componentes Clave

### Integración de Sensores de Contacto
- URDF de Franka Panda modificado con 8 sensores de contacto (4 por dedo)
- Visualización de fuerza en tiempo real y recopilación de datos
- Retroalimentación táctil para tareas de manipulación

### Scripts Principales
- `lift_cube_sm_with_sensors.py` - Máquina de estados para el levantamiento de objetos con retroalimentación de sensores
- `static_force_test.py` - Pruebas de fuerza estática y calibración
- Diversas herramientas de análisis y visualización

## Primeros Pasos

1. Instale Isaac Lab (siga la documentación oficial)
2. Navegue a `cabinet_sensor_project/` para instrucciones de uso detalladas
3. Ejecute los experimentos utilizando los scripts de shell proporcionados

## Características

- Visualización de la fuerza de contacto en tiempo real
- Cálculo del promedio de fuerza paso a paso
- Registro exhaustivo de datos de los sensores
- Control de manipulación basado en máquinas de estados

## Documentación

Consulte las carpetas de los proyectos individuales para obtener documentación detallada y guías de uso.

## Dependencias

- Isaac Lab
- PyTorch
- NumPy
- Matplotlib
- OpenCV (para visualización)

---

*Desarrollado para la investigación robótica y aplicaciones de detección táctil*
