from django.conf import settings
import easyocr
import re
import os
import numpy as np
from PIL import Image
import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pdf2image import convert_from_path
import tempfile

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_file):
    """Extract text from image or PDF"""
    images = []
    
    if hasattr(image_file, 'name') and image_file.name.lower().endswith('.pdf'):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            for chunk in image_file.chunks():
                temp_pdf.write(chunk)
            temp_pdf_path = temp_pdf.name
        
        try:
            pdf_images = convert_from_path(
                temp_pdf_path,
                dpi=600,
                poppler_path=settings.POPPLER_PATH,
                first_page=1,
                last_page=1
            )
            images.extend(pdf_images)
            os.unlink(temp_pdf_path)
        except Exception as e:
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
            return None
    else:
        images = [Image.open(image_file)]

    all_results = []
    for image in images:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        img_array = np.array(Image.open(img_byte_arr))
        results = reader.readtext(img_array)
        all_results.extend(results)
    
    return ' '.join([text[1] for text in all_results])


@api_view(['POST'])
def extract_dates_api(request):
    """API endpoint to extract all dates from an image or PDF"""
    if 'image' not in request.FILES:
        return Response({'error': 'No image or PDF file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['image']
    file_extension = os.path.splitext(file.name)[1].lower() if hasattr(file, 'name') else ''
    
    if file_extension not in ['.jpg', '.jpeg', '.png', '.pdf']:
        return Response({'error': 'Unsupported file format. Please upload JPG, JPEG, PNG, or PDF'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    extracted_text = extract_text_from_image(file)
    
    if not extracted_text:
        return Response({'error': 'Failed to process file or extract text'}, status=status.HTTP_400_BAD_REQUEST)
    
    date_patterns = [
        r'\b([0-3]?[0-9][/.-][0-1]?[0-9][/.-](19|20)?[0-9]{2})\b',
        r'\b([0-1]?[0-9][/.-][0-3]?[0-9][/.-](19|20)?[0-9]{2})\b',
        r'\b((19|20)[0-9]{2}[/.-][0-1]?[0-9][/.-][0-3]?[0-9])\b',
    ]
    
    found_dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, extracted_text)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    found_dates.append(match[0])
                else:
                    found_dates.append(match)
    
    found_dates = list(set(found_dates))
    
    return Response({
        'dob': found_dates
    }, status=status.HTTP_200_OK)