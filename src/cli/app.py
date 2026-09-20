from .context import AppContext
from .router import Router


def main():
    context = AppContext()
    router = Router(context)
    router.run()


if __name__ == "__main__":
    main()
