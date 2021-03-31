import onnx
#from onnx import version_converter,helper


# Load the model
converted_model = onnx.load("fcn-resnet50-11.onnx")
model=converted_model
#check
if model != None:
    print("model loaded true")
    print("Version:",model.MODEL_VERSION_FIELD_NUMBER)
    print("OpSetVersion:",model.OPSET_IMPORT_FIELD_NUMBER)
    print("ProducerVersion:",model.PRODUCER_VERSION_FIELD_NUMBER)
    #print(model.GRAPH_FIELD_NUMBER)
    #input("press")
    #print("The model before conversion:\n{}".format(model))
    

# Check that the IR is well formed
onnx.checker.check_model(model)

from onnx import version_converter
input("enter to convert")
# Convert to version
converted_model9 = version_converter.convert_version(converted_model,9)

input("enter to save")
# Save model
onnx.save(converted_model9, "fcn-resnet50-9.onnx")
print("done..")
