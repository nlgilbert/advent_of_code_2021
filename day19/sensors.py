from dataclasses import dataclass

def get_num_overlaps(beacons_1, beacons_2):
    num_overlaps = 0
    for beacon in beacons_1:
        if beacon in beacons_2:
            num_overlaps += 1
    return num_overlaps

@dataclass
class Beacon:
    x: int
    y: int
    z: int

    def translate(self, translation):
        self.x += translation[0]
        self.y += translation[1]
        self.z += translation[2]
        return self

    def rotate(self, rotation):
        assert rotation[0] in [-90, 0, 90, 180]
        assert rotation[1] in [-90, 0, 90, 180]
        assert rotation[2] in [-90, 0, 90, 180]

        # Rotate around x
        if rotation[0] == 90:
            self.y, self.z = (-self.z, self.y)
        elif rotation[0] == 180:
            self.y, self.z = (-self.y, -self.z)
        elif rotation[0] == -90:
            self.y, self.z = (self.z, -self.y)

        # Rotate around y
        if rotation[1] == 90:
            self.x, self.z = (self.z, -self.x)
        elif rotation[1] == 180:
            self.x, self.z = (-self.x, -self.z)
        elif rotation[1] == -90:
            self.x, self.z = (-self.z, self.x)

        # Rotate around z
        if rotation[2] == 90:
            self.x, self.y = (-self.y, self.x)
        elif rotation[2] == 180:
            self.x, self.y = (-self.x, -self.y)
        elif rotation[2] == -90:
            self.x, self.y = (self.y, -self.x)
        
        return self
            

class Scanner:

    def __init__(self, beacons):
        self.beacons = beacons
        self.translation = None
        self.rotation = None
    
    def get_transformed_beacons(self, translation, rotation):
        transformed_beacons = []
        for beacon in self.beacons[:]:
            new_beacon = Beacon(beacon.x, beacon.y, beacon.z)
            new_beacon.rotate(rotation)
            new_beacon.translate(translation)
            transformed_beacons.append(new_beacon)
        return transformed_beacons
    
    def set_transformation(self, translation, rotation):
        self.beacons = self.get_transformed_beacons(translation, rotation)
        self.translation = translation
        self.rotation = rotation

    def try_align(self, reference):
        rotations = []
        for rot_x in [-90, 0, 90, 180]:
            for rot_y in [-90, 0, 90, 180]:
                for rot_z in [-90, 0, 90, 180]:
                    rotations.append((rot_x, rot_y, rot_z))
        
        for rotation in rotations:
            for ref_beacon in reference.beacons:
                for beacon in self.get_transformed_beacons((0, 0, 0), rotation)[11:]:
                    translation = (
                        ref_beacon.x - beacon.x,
                        ref_beacon.y - beacon.y,
                        ref_beacon.z - beacon.z
                    )
                    beacons_t = self.get_transformed_beacons(translation, rotation)
                    # num_overlaps = get_num_overlaps(beacons_t, reference.beacons)
                    # print(num_overlaps)
                    if get_num_overlaps(beacons_t, reference.beacons) >= 12:
                        # Successful alignment
                        self.set_transformation(translation, rotation)
                        return True
        return False

def main():
    scanner = Scanner([Beacon(1, 2, 3), Beacon(1, 1, 1)])
    # print(Beacon(1, 2, 3) in beacons_1)
    # print(Beacon(2, 3, 4).translate((-1, -1, -1)))
    # print(Beacon(2, 3, 4).translate((-1, -1, -1)) in scanner.beacons)
    # print(Beacon(1, 2, 3).rotate((0, 180, 90)))
    # print(scanner.get_transformed_beacons((-10, 0, 0), (0, 180, 90)))
    ref_beacon = Beacon(-6, 3, 8)
    beacon = Beacon(1, 1, 1).rotate((0, 180, 90))
    print(beacon)
    translation = (
        ref_beacon.x - beacon.x,
        ref_beacon.y - beacon.y,
        ref_beacon.z - beacon.z
    )
    print(scanner.get_transformed_beacons(translation, (0, 180, 90)))
    print(scanner.beacons)


if __name__ == '__main__':
    main()