def collision_2d(ax, az, bx, bz, threshold=1):
    return abs(ax - bx) < threshold and abs(az - bz) < threshold