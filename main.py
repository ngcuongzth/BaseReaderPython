from core.ImageProcessor import ImageProcessor
from core.QRCodeProcessor import QRCodeProcessor

Processor = ImageProcessor(is_init_dnn_superres=True)
Reader = QRCodeProcessor(is_init_qreader=True)

image = Processor.readImage("./dbr/1.png")
image_processed = Processor.useSuperResolution(image)
Processor.showImage("w", image)


data = Reader.useQReaderProcessorDecode(image_processed, 2)
print(data)
