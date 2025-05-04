// Función genérica para hacer peticiones
const API_BASE_URL = process.env.URL;


const fetchApi = async (endpoint, method = 'GET', body = null, headers = {}) => {
    const url = `${API_BASE_URL}${endpoint}`;

    const config = {
        method,
        headers: {
            'Content-Type': 'application/json',
            ...headers
        },
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error en la petición:', error);
        throw error;
    }
};

// Métodos específicos
export const apiService = {
    // GET - Obtener datos
    get: async (endpoint, headers = {}) => {
        return fetchApi(endpoint, 'GET', null, headers);
    },

    // POST - Enviar datos
    post: async (endpoint, data, headers = {}) => {
        return fetchApi(endpoint, 'POST', data, headers);
    },

    // PUT - Actualizar datos (por si lo necesitas)
    put: async (endpoint, data, headers = {}) => {
        return fetchApi(endpoint, 'PUT', data, headers);
    },

    // DELETE - Eliminar datos (por si lo necesitas)
    delete: async (endpoint, headers = {}) => {
        return fetchApi(endpoint, 'DELETE', null, headers);
    }
};