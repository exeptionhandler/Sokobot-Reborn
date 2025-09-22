# 🎮 Sokoromi - Bot de Sokoban Kawaii para Discord

<div align="center">
  <img src="https://img.shields.io/badge/Python-100%25-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Discord-Bot-7289da?style=for-the-badge&logo=discord&logoColor=white" alt="Discord Bot">
  <img src="https://img.shields.io/badge/Sokoban-Kawaii-ff69b4?style=for-the-badge" alt="Sokoban Kawaii">
</div>

---

## ✨ Descripción

**Sokoromi** es un adorable bot de Discord que trae el clásico juego de rompecabezas **Sokoban** directamente a tu servidor con un toque kawaii único. Disfruta de mapas infinitos generados aleatoriamente, compite en tablas de clasificación globales y personaliza tu experiencia con una interfaz súper kawaii.

### 🌟 Características Principales

- 🗺️ **Mapas infinitos aleatorios** - Nunca te quedarás sin desafíos
- 📊 **Sistema de puntuación y estadísticas** - Rastrea tu progreso
- 🏆 **Tabla de clasificación global** - Compite con jugadores de todo el mundo  
- 🎨 **Interfaz kawaii personalizable** - Hace que cada partida sea adorable
- 🎮 **Controles intuitivos** - Fácil de jugar para todos
- 📱 **Soporte multiplataforma** - Funciona en móvil, escritorio y consola
- ⚡ **Comandos slash** - Interfaz moderna de Discord

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- Una aplicación de Discord creada en el [Portal de Desarrolladores](https://discord.com/developers/applications)

### Pasos de Instalación

Clona el repositorio
~~~
git clone https://github.com/exeptionhandler/Sokoromi.git
~~~

Navega al directorio
~~~
cd Sokoromi
~~~
Crea un entorno virtual
~~~
python -m venv sokoromi-env
~~~
Activa el entorno virtual
En Windows:
~~~
sokoromi-env\Scripts\activate
~~~
En Linux/macOS:
~~~
source sokoromi-env/bin/activate
~~~
Instala las dependencias
~~~
pip install -r requirements.txt
~~~
text

## ⚙️ Configuración

1. Crea un archivo `.env` en el directorio raíz:
TOKEN=tu_token_de_bot_aqui
PREFIX=/

2. Invita el bot a tu servidor con los permisos necesarios:
   - Enviar mensajes
   - Usar comandos de aplicación
   - Insertar enlaces
   - Leer historial de mensajes

3. Ejecuta el bot:
~~~
python main.py
~~~
## 🎯 Comandos Principales

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/play` | Inicia una nueva partida | `/play` |
| `/stop` | Terminar partida actual | `/stop` |
| `/info` | Muestra todos los comandos disponibles | `/info` |

### 🕹️ Controles de Juego
- **W/↑** - Mover arriba
- **A/←** - Mover izquierda  
- **S/↓** - Mover abajo
- **D/→** - Mover derecha
- **🔄** - Reiniciar nivel
- **❌** - Terminar partida

## 🎨 Capturas de Pantalla
<img width="382" height="318" alt="image" src="https://github.com/user-attachments/assets/764635ac-b394-4440-8c1f-99ea2b8ead63" />


## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar Sokoromi:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commitea tus cambios (`git commit -m 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request


## 🐛 Reportar Problemas

¿Encontraste un bug? ¡Ayúdanos a mejorar!
- Abre un [issue](https://github.com/exeptionhandler/Sokoromi/issues)
- Describe el problema detalladamente
- Incluye pasos para reproducir el error

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🎀 Créditos

- Desarrollado con ❤️ por [exeptionhandler](https://github.com/exeptionhandler)
- Basado en el clásico juego Sokoban
- Construido con [discord.py](https://discordpy.readthedocs.io/)

---

<div align="center">
  <p>⭐ ¡No olvides darle una estrella al repo si te gusta Sokoromi! ⭐</p>
  
  **¿Tienes preguntas?** ¡Únete a nuestro [servidor de Discord](https://discord.gg/269J9TU6Gp) para soporte!
</div>
