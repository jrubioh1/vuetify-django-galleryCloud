import { createI18n } from 'vue-i18n';

// Traducciones
const messages = {
  en: {
    title_app: 'CloudGallery',
    title_staistics1: 'Image Statistics by Year and Month',
    noData: 'No Images Data',
    upload:'Upload images',
    images:'Images',
    staistics:'Staistics',
    selectImages: 'Please select images to upload',
    tooManyFiles: 'You cannot select more than 1000 files.',
    uploadSuccess: 'Images uploaded successfully',
    uploadError: 'Error uploading images',
    fileUpload: {
      defaultText: 'Click here to upload files',
    },
    imagespage: {
    noImages: "No images available",
    deleteSelected: "Delete selected",
    refresh: "Refresh",
    selectAll: "Select all",
    deselectAll: "Deselect all",
    downloadSelected: "Download selected",
    filterYear: "Filter year",
    filterMonth: "Filter month",
    uploadedAt: "Uploaded at",
    deleteImage: "Delete image",
    downloadImage: "Download image",
    monthYear: "{month} {year}"
  }

  },
  es: {
    title_app: 'Galería Nube',
    title_staistics1: 'Estadísticas de Imágenes por Años y Meses',
    noData: 'Sin datos de imágenes',
    upload:'Subir imágenes',
    images:'Imágenes',
    staistics:'Estadísticas',
    selectImages: 'Por favor selecciona imágenes para subir',
    tooManyFiles: 'No puedes seleccionar más de 1000 archivos.',
    uploadSuccess: 'Imágenes subidas con éxito',
    uploadError: 'Error al subir imágenes',
    fileUpload: {
        defaultText: 'Haz clic aquí para subir archivos',
      },
      imagespage: {
    noImages: "No hay imágenes disponibles",
    deleteSelected: "Eliminar seleccionados",
    refresh: "Actualizar",
    selectAll: "Seleccionar todos",
    deselectAll: "Deseleccionar todos",
    downloadSelected: "Descargar seleccionados",
    filterYear: "Filtrar por año",
    filterMonth: "Filtrar por mes",
    uploadedAt: "Subido el",
    deleteImage: "Eliminar imagen",
    downloadImage: "Descargar imagen",
    monthYear: "{month} {year}"
  }

  },
};

const i18n = createI18n({
  legacy:false,
  locale: 'en', // Idioma predeterminado
  fallbackLocale: 'en', // Idioma de respaldo
  messages, // Traducciones
});

export default i18n;