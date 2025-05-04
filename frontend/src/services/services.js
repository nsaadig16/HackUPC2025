import { apiService } from './serviceapi';

export async function finish() {

    try {
        const data = await apiService.post('/finish');
        console.log('Data fetched:', data);
        // Aquí puedes hacer algo con los datos obtenidos
        return data;

    } catch (error) {
        console.error('Error fetching data:', error);
    }


}

export async function travel(formData) {
    try {
        const data = await apiService.post('/travel', formData);
        return data;

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

export async function get_num_travels() {
    try {
        const data = await apiService.get('/get_num_travels');
        return data;

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

export async function get_travels() {
    try {
        const data = await apiService.get('/get_travels');
        return data;

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

