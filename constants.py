"""
Constants for VehiLog application.

This module contains all constant values used throughout the application,
including form choices, validation options, and other static data.
"""

# =============================================================================
# Vehicle Form Choices
# =============================================================================

VEHICLE_TYPE_CHOICES = [
    ('MCWG', 'Motorcycle with Gear'),
    ('MCWOG', 'Motorcycle without Gear'),
    ('LMV', 'Light Motor Vehicle'),
    ('HMV', 'Heavy Motor Vehicle')
]

FUEL_TYPE_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('Electric', 'Electric'),
    ('CNG', 'CNG')
]

POLICY_TYPE_CHOICES = [
    ('', 'Select Policy Type'),
    ('Comprehensive', 'Comprehensive'),
    ('Third Party', 'Third Party'),
    ('Standalone OD', 'Standalone Own Damage')
]

# =============================================================================
# Complete RTO Office List for India
# =============================================================================

# Tamil Nadu RTO Offices (Official List)
TN_RTO_OFFICE_CHOICES = [
    ('', 'Select RTO Office'),
    ('TN01', 'TN01 - Chennai Central'),
    ('TN02', 'TN02 - Chennai North West'),
    ('TN03', 'TN03 - Chennai North East'),
    ('TN04', 'TN04 - Chennai East'),
    ('TN05', 'TN05 - Chennai North'),
    ('TN06', 'TN06 - Chennai South East'),
    ('TN07', 'TN07 - Chennai South'),
    ('TN09', 'TN09 - Chennai West'),
    ('TN10', 'TN10 - Chennai South West'),
    ('TN11', 'TN11 - Tambaram'),
    ('TN12', 'TN12 - Paruthipattu'),
    ('TN13', 'TN13 - Ambattur'),
    ('TN14', 'TN14 - Sholinganallur'),
    ('TN15', 'TN15 - Uludurpet'),
    ('TN16', 'TN16 - Tindivanam & Enforcement Wing'),
    ('TN18', 'TN18 - Red Hills'),
    ('TN19', 'TN19 - Chengalpattu'),
    ('TN20', 'TN20 - Thiruvallur'),
    ('TN21', 'TN21 - Kanchipuram'),
    ('TN22', 'TN22 - Meenambakkam'),
    ('TN23', 'TN23 - Vellore'),
    ('TN24', 'TN24 - Krishnagiri'),
    ('TN25', 'TN25 - Tiruvannamalai'),
    ('TN28', 'TN28 - Namakkal North'),
    ('TN29', 'TN29 - Dharmapuri'),
    ('TN30', 'TN30 - Salem West'),
    ('TN31', 'TN31 - Cuddalore'),
    ('TN32', 'TN32 - Viluppuram'),
    ('TN33', 'TN33 - Erode East'),
    ('TN34', 'TN34 - Tiruchengode'),
    ('TN36', 'TN36 - Gobi'),
    ('TN37', 'TN37 - Coimbatore South'),
    ('TN38', 'TN38 - Coimbatore North'),
    ('TN39', 'TN39 - Tirpur North'),
    ('TN40', 'TN40 - Mettupalayam'),
    ('TN41', 'TN41 - Pollachi'),
    ('TN42', 'TN42 - Tirupur South'),
    ('TN43', 'TN43 - Ooty'),
    ('TN45', 'TN45 - Trichy West'),
    ('TN46', 'TN46 - Perambalur'),
    ('TN47', 'TN47 - Karur'),
    ('TN48', 'TN48 - Srirangam'),
    ('TN49', 'TN49 - Thanjavur'),
    ('TN50', 'TN50 - Tiruvarur'),
    ('TN51', 'TN51 - Nagapattinam'),
    ('TN52', 'TN52 - Sankagiri'),
    ('TN54', 'TN54 - Salem East'),
    ('TN55', 'TN55 - Pudukottai'),
    ('TN56', 'TN56 - Perundurai'),
    ('TN57', 'TN57 - Dindigul'),
    ('TN58', 'TN58 - Madurai South'),
    ('TN59', 'TN59 - Madurai North'),
    ('TN60', 'TN60 - Theni'),
    ('TN61', 'TN61 - Ariyalur'),
    ('TN63', 'TN63 - Sivangangai'),
    ('TN64', 'TN64 - Madurai Central'),
    ('TN65', 'TN65 - Ramanathapuram'),
    ('TN66', 'TN66 - Coimbatore Central'),
    ('TN67', 'TN67 - Virudhnagar'),
    ('TN68', 'TN68 - Kumbakonam'),
    ('TN69', 'TN69 - Tuticorin'),
    ('TN70', 'TN70 - Hosur'),
    ('TN72', 'TN72 - Tirunelveli'),
    ('TN73', 'TN73 - Ranipet'),
    ('TN74', 'TN74 - Nagercoil'),
    ('TN75', 'TN75 - Marthandam'),
    ('TN76', 'TN76 - Tenkasi'),
    ('TN77', 'TN77 - Attur'),
    ('TN78', 'TN78 - Dharapuram'),
    ('TN79', 'TN79 - Sankarankovil'),
    ('TN81', 'TN81 - Trichy East'),
    ('TN82', 'TN82 - Mayiladuthurai'),
    ('TN83', 'TN83 - Vaniyambadi'),
    ('TN83M', 'TN83M - Tirupattur'),
    ('TN84', 'TN84 - Srivilliputtur'),
    ('TN85', 'TN85 - Kundrathur'),
    ('TN86', 'TN86 - Erode West'),
    ('TN87', 'TN87 - Sriperumudur'),
    ('TN88', 'TN88 - Nammakal South'),
    ('TN90', 'TN90 - Salem South'),
    ('TN91', 'TN91 - Chidambaram'),
    ('TN92', 'TN92 - Tiruchendur'),
    ('TN93', 'TN93 - Mettur'),
    ('TN94', 'TN94 - Palani'),
    ('TN95', 'TN95 - Sivakasi'),
    ('TN96', 'TN96 - Kovilpatti'),
    ('TN97', 'TN97 - Arani'),
    ('TN99', 'TN99 - Coimbatore West'),
]

# All RTO choices (currently only TN, can be extended for other states)
RTO_OFFICE_CHOICES = TN_RTO_OFFICE_CHOICES

# =============================================================================
# Other Constants
# =============================================================================

# File upload settings
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Date format
DATE_FORMAT = '%d/%m/%Y'

# Validation constants
MIN_YEAR = 1990
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 80
MIN_PASSWORD_LENGTH = 6