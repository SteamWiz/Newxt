# Newxt

## Edit files in one pass with instructions via stdin

The following document is for _developers_ contributing to the application. For information about how to _use_ the application, see PACKAGE.md.

## Development setup

Requires Python 3.13 or higher. Uses [Dyngle](https://dyngle.steamwiz.io/) for administration (installed separately). Shared Dyngle operations live in the `.conf` submodule ([SteamWiz/Conf](https://github.com/SteamWiz/Conf)), so clone with `--recurse-submodules` or run `git submodule update --init`.

- `dyngle run init` - Create the virtual environment and install poetry
- `dyngle run dependencies` - Install the required packages using poetry
- `dyngle run test` - Run tests and report coverage (same as CI/CD)
- `dyngle run style` - Run style checks
- `dyngle run build` - Create a test build

GitHub Actions performs the entire build/test/release cycle using the shared [SteamWiz actions](https://github.com/SteamWiz/actions).

## Libraries

The application uses the following external libraries:

- [WizLib](https://wizlib.steamwiz.io/) for CLI and configuration handling

<br/>

---

<br/>

<!--<a href="https://www.flaticon.com/free-icons/particles" title="particles icons">Particles icon by Freepik-Flaticon</a>-->
