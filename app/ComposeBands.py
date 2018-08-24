import os
import sys


class ComposeBands:
    """."""

    def __init__(self, input_dir, output_dir, output_file_name):
        """Init.

        Argument:
            input_dir [str] -- The path where all images are.
            output_dir [str] -- The path where compose image will be saved.
            output_file_name [str] -- Name of file without extension.
        """
        self.input_dir = input_dir

        self.output_dir = output_dir

        self.output_file_name = output_file_name

    def stack_img(self, expression, extension):
        """Stacking bands from landsat in tmp folder.

        Argument:
            expression (str) -- Regular expression which select files who will
                                be put in output.
            extension (str) -- Types of extensions output file ['.TIF', '.img']
        """
        # Path where band files can be find.
        # Here, it is the input for gdal_merge.
        input_img_dir = os.path.join(self.input_dir, expression)

        # Output image
        output_image_path = os.path.join(self.output_dir,
                                         self.output_file_name + extension)

        command = 'gdal_merge.py -separate -a_nodata 0 -o ' \
                  ' {output_image_path} {input_img_dir}' \
                  .format(output_image_path=output_image_path,
                          input_img_dir=input_img_dir)
        os.system(command)

    def stack_sentinel(self, scene_file_name, utm_zone):
        """.

        Arg:
            variable (type): description

        Return:
            type: description

        Raise:
            Exception: description

        """
        path = self.input_dir
        os.chdir(path)
        command = 'gdal_translate SENTINEL2_L1C:{scene_file_name}.SAFE/' \
                  'MTD_MSIL1C.xml:10m:EPSG_327{utm_zone} -ot Byte -scale ' \
                  '{output_file_name}.TIF --config ' \
                  'GDAL_CACHEMAX 1000 --config GDAL_NUM_THREADS ALL_CPUS ' \
                  '-co COMPRESS=DEFLATE' \
                  .format(scene_file_name=scene_file_name,
                          utm_zone=utm_zone,
                          output_file_name = self.output_file_name)

        os.system(command)
