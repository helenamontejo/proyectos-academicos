import asyncio
import httpx

BASE_URL = "http://127.0.0.1:5000/api/v1/masajes"

async def main():
    async with httpx.AsyncClient() as client:

        #GET
        print("\n--- LISTANDO MASAJES ---")
        resp = await client.get(BASE_URL)
        print(resp.json())

        #POST
        print("\n--- CREANDO MASAJE ---")
        nuevo = {
            "nombre": "Masaje cliente",
            "duracion": 30,
            "precio": 50,
            "individual": True,
            "user_id": "cliente-test",
            "filename": None
        }

        resp = await client.post(BASE_URL, json=nuevo)

        if resp.status_code != 201:
            print("ERROR:", resp.text)
            return

        print(resp.json())

        masaje_creado = resp.json()
        masaje_id = masaje_creado.get("id")

        #GET por ID
        print("\n--- OBTENER MASAJE ---")
        resp = await client.get(f"{BASE_URL}/{masaje_id}")
        print(resp.json())

        #DELETE
        print("\n--- ELIMINANDO MASAJE ---")
        resp = await client.delete(f"{BASE_URL}/{masaje_id}")
        print(resp.json())


if __name__ == "__main__":
    asyncio.run(main())