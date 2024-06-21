from core.DatamatrixProcessor import DatamatrixProcessor
from core.ImageProcessor import ImageProcessor


Reader = DatamatrixProcessor()
Processor = ImageProcessor(is_init_dnn_superres=True)

image = Processor.readImage("./images/datamatrix/datamatrix2.png")
image_processed = Processor.useSuperResolution(image)
data = Reader.useLoopReader(image_processed)

print(data)
