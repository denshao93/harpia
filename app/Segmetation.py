import os #NOQA

class Segmentation:
    
    algo="SLICO"

    def __init__(self, tmp_dir, output_dir, output_file_name):

        self.algo="SLIC"

        self.tmp_dir = tmp_dir

        # The folder where output processed is stored.
        self.output_dir = output_dir

        # Name of image file save the will be segmented.
        self.output_file_name = output_file_name

    def get_segmentation(self, r, i, algo):
        """Segmentation function by gdal-segment
        Arguments:
            region {int} -- r
            inter {int} -- Number of Interatiction
            algorithm {str} -- Kinds of segmentation which gdal-segment offers -
                               <LSC, SLICO, SLIC, SEEDS, MSLIC>
        """

        print("........Segmentanção.........")
      
        input_img = os.path.join(self.output_dir, f"{self.output_file_name}.TIF")
        output_segmentation = os.path.join(self.tmp_dir, f"{self.output_file_name}_{algo}.shp")
        
        command = f"$HOME/gdal-segment/bin/gdal-segment -region {r} -niter {i} "\
                  f"-algo {algo} {input_img} -out {output_segmentation}"
        
        os.system(command)

    def get_segmentation_path(self):
        
        output_segmentation = os.path.join(self.output_dir, f"{self.output_file_name}_{self.algo}.shp")
        
        return output_segmentation