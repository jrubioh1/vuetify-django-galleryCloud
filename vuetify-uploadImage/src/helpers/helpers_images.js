import {axiosWrapper} from '@/helpers/axiosWrapper.js'
import { useAppStore } from '@/stores/app';

const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  
function getMonthNameList(monthNumberList) {

    return monthNumberList.map(monthNumber=>{ return monthNames[parseInt(monthNumber, 10) - 1];}) // Convertir número de mes a índice
  }
  function getMonthName(monthNumber) {
    
    return  monthNames[parseInt(monthNumber, 10) - 1]; // Convertir número de mes a índice
  }
  function getMonthNumber(monthName) {
  
    const index = monthNames.indexOf(monthName);
    return index !== -1 ? String(index + 1).padStart(2, '0') : null; // Convierte a 2 dígitos
  }

 async function download_image(id, apiUrl) {
  try {
    const response = await axiosWrapper.get(`${apiUrl}uploads/download_image/?id=${id}`, {
      responseType: 'blob',
    });
    const blob = response.data;
    const blobUrl = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = 'image.jpg'; // Cambia esto según el nombre del archivo deseado
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error downloading image:', error);
  }
}


async function download_selected(selectedIds, apiUrl) {
  try {
    const formData = new FormData();
    selectedIds.forEach(id => formData.append('id', id));

    const response = await axiosWrapper.post(`${apiUrl}uploads/download_selected/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      responseType: 'blob',
    });

    const blob = new Blob([response.data], { type: 'application/zip' });
    const blobUrl = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = blobUrl;
    link.download = 'selected_images.zip';
    link.click();
    link.remove();
  } catch (error) {
    console.error('Error downloading selected images:', error);
  }
}


async function delete_selected(selectedIds, apiUrl) {
  try {
    const formData = new FormData();
    selectedIds.forEach(id => formData.append('id', id));

    const response = await axiosWrapper.delete(`${apiUrl}uploads/delete/`, {
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    useAppStore().get_images_by_year_month()
    console.log('Deleted images response:', response.data);
  } catch (error) {
    console.error('Error deleting selected images:', error);
  }
}

async function delete_image(id, api) {
    try {
      const formData = new FormData()
      formData.append('id', id)
      const response = await axiosWrapper.delete(api + 'uploads/delete_image/', { data: formData }, { headers: { 'Content-Type': 'multipart/form-data' } })
      console.log(response.data)
      useAppStore().get_images_by_year_month()
  
    } catch (error) {
      console.error(error)
    }
  
  }

  function select_all(imagesFiltered) {
    let selected = []; // Vacía la selección inicial
    // Iterar sobre los años
    Object.entries(imagesFiltered).forEach(([year, months]) => {
      // Iterar sobre los meses dentro de cada año
      Object.entries(months).forEach(([month, images]) => {
        // Agregar los IDs de las imágenes al array seleccionado
        images.forEach(image => {
          selected.push(image.id);
        });
      });
    });
    return selected;
  }

export {getMonthName, getMonthNumber,getMonthNameList, delete_selected, download_selected, download_image, delete_image, select_all}
  