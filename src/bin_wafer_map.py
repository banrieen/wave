import wafermap
import time

start = time.time()

wm = wafermap.WaferMap(wafer_radius=100,                # all length dimensions in mm
                       cell_size=(10, 20),              # (sizeX, sizeY)
                       cell_margin=(8, 15),             # distance between cell borders (x, y)
                       cell_origin=(0, 0),              # which cell to select as origin (0, 0), in (x, y)
                       grid_offset=(-2.05, -4.1),       # grid offset in (x, y)
                       edge_exclusion=2.2,              # margin from the wafer edge where a red edge exclusion ring is drawn
                       coverage='full',                 # 'full': will cover wafer with cells, partial cells allowed
                                                        # 'inner': only full cells allowed
                       notch_orientation=270)           # angle of notch in degrees. 270 corresponds to a notch at the bottom

# wm.add_image(image_source_file="inspection1.jpg",
#              cell=(1, 0),                               # (cell_index_x, cell_index_y)
#              offset=(2.0, 2.0))                         # relative coordinate of the image within the cell

# # save to html
# wm.save_html(f"wafermap.html")

# save to png (Chromium must be installed)

wm.save_png(f"wafermap.png")
end = time.time()

print(f"Iteration: start time: {start}, end time: {end}, taken: {(end-start)} s")