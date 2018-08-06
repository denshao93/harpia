import os #NOQA

class Segmentation:
    
    def __init__(self, output_dir, output_file_name):

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
        output_segmentation = os.path.join(self.output_dir, f"{self.output_file_name}_{algo}.shp")
        
        command = f"$HOME/gdal-segment/bin/gdal-segment -region {r} -niter {i} "\
                  f"-algo {algo} {input_img} -out {output_segmentation}"
        
        os.system(command)

    def run_segmentation(self):
        """
        Segmenting landsat image
        """
        self.get_segmentation(r=5, i=10, algo="SLICO")
