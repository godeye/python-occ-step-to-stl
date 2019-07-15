def read_step(filename):
    from OCC.STEPControl import STEPControl_Reader
    from OCC.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity

    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)
    if status == IFSelect_RetDone:
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity) 

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        return step_reader.Shape(1)
    else:
        raise ValueError('Cannot read the file')

def write_stl(shape, filename, definition=0.1):
    from OCC.StlAPI import StlAPI_Writer
    import os

    directory = os.path.split(__name__)[0]
    stl_output_dir = os.path.abspath(directory)
    assert os.path.isdir(stl_output_dir)

    stl_file = os.path.join(stl_output_dir, filename)

    stl_writer = StlAPI_Writer()
    stl_writer.SetASCIIMode(False)

    from OCC.BRepMesh import BRepMesh_IncrementalMesh
    mesh = BRepMesh_IncrementalMesh(shape, definition)
    mesh.Perform()
    assert mesh.IsDone()

    stl_writer.Write(shape, stl_file)
    assert os.path.isfile(stl_file)


shape = read_step('example.step')

write_stl(shape, 'example.stl')

