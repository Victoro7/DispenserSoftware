# Tip and Reservoir volumes
tube_5mL = 5000.000
tube_1500uL = 1500.000
res_25mL = 25000.000
tip_250 = 250

# 96 Well Plate Coordinates
plate_96 = [125, 20]
plate96_movement_height = 49
dispense_height_EZ = 53
dispense_height_96 = None

# 6 Well Plate Coordinates
plate_6 = []
plate6_movement_height = None
dispense_height_3in1 = None
dispense_height_6 = None

# 25 mL Reservoir Coordinates
pos_reservoir_25ml = [3, 58]
aspirate_height_25ml = 56
movement_height_25mL = 36

# 1.5 mL Reservoir Coordinates
tubes4tips = [[]]
tubes2tips = []
aspirate_height_1_5ml = None
movement_height_1_5ml = None

# Ejection Coordinates
eject_bowl = [5, 108]
eject_height = 66

# Presenting Coordinates
present = [65, 0]
present_height = 0

# Equipping Coordinates
tip_tray_8 = []
equip_height = None


# 96-well plate volume array dimensions
dims_96 = (8, 12)

# No. of dispensing zones in 96-well plate
zone_96 = 96

# No. of tips for 2 tip dispensing
tip2 = 2

# No. of tips for 4 tip dispensing
tip4 = 4

# No. of reservoirs
rnum1 = 1
rnum4 = 4
rnum8 = 8

# Indexes
x = 0
y = 1

# Calibration and Testing Coordinates
beaker = [22.5, 61]
beaker_asp_height = 60
cal_tubes8 = [[9, 104], [27, 104], [45, 104], [72, 104], [0, 117], [18, 117], [36, 117], [54, 117]]
cal_tubes4 = [[9, 104], [45, 104], [0, 117], [36, 117]]
tubes_disp_height = 45
cal_movement_height = 10
dispense_move_height = 40
zero_height = 0 # Find height, set manually with G92 E

# Calibration model dispensing factor
model_factor = 1

