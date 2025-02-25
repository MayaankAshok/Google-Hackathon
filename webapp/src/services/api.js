export const uploadImage = async (file) => {
  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Upload failed');
    }

    return await response.json();
  } catch (error) {
    throw new Error(`Upload error: ${error.message}`);
  }
};

export const getSimilarMedicines = async (medicineName) => {
  try {
    const response = await fetch('http://localhost:5000/similar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ medicine: medicineName }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch similar medicines');
    }

    return await response.json();
  } catch (error) {
    throw new Error(`Similar medicines error: ${error.message}`);
  }
};
