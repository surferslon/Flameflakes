import uvicorn


def main() -> None:
    uvicorn.run("server:app", port=9090, reload=True)


if __name__ == "__main__":
    main()
