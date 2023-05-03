const BASE_URL = import.meta.env.VITE_BASE_URL

interface IResponse {
  success: boolean;
  status: number;
  error: any;
  result: {
    token: string
  },
}

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

export const login = async (data: { email: string, password: string, username: string }): Promise<null | IResponse> => {
  try {
    const url = `${BASE_URL}/login`;
    const request = await fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
    });
    const response = await request.json()
    return {
      ...response,
      status: request?.status
    }
  } catch (error) {
    return null
  }
}