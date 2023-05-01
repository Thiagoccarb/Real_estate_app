const BASE_URL = import.meta.env.VITE_BASE_URL

export const submitCredentials = async (data: { email: string, password: string, username: string }) => {
  try {
    const url = `${BASE_URL}/users`;
    const request = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    });

    return request;

  } catch (error) {
    return null
  }
}