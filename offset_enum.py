from enum import IntEnum


class OffsetValues(IntEnum):
    """
        Class mapping x & y screen coordinates for extracting raw text from
        match picture
    """
    # Score Board Coordinates
    scoreboard_upper_y = 1260
    scoreboard_lower_y = 1450
    scoreboard_left_x = 110
    scoreboard_right_x = 760

    # Header Coordinates
    header_upper_y = 1275
    header_lower_y = 1325
    header_left_x = 135
    header_right_x = 550

    # Competitor 1 Name
    competitor_1_name_upper_y = 1325
    competitor_1_name_lower_y = 1380
    competitor_1_name_left_x = 135
    competitor_1_name_right_x = 590

    # Competitor 2 Name
    competitor_2_name_upper_y = 1385
    competitor_2_name_lower_y = 1440
    competitor_2_name_left_x = 135
    competitor_2_name_right_x = 590

    # Competitor 1 Points
    competitor_1_points_upper_y = 1335
    competitor_1_points_lower_y = 1370
    competitor_1_points_left_x = 625
    competitor_1_points_right_x = 660

    # Competitor 2 Points
    competitor_2_points_upper_y = 1395
    competitor_2_points_lower_y = 1428
    competitor_2_points_left_x = 622
    competitor_2_points_right_x = 663

    # Competitor 1 Advantages &/or Penalties
    competitor_1_ads_or_pens_upper_y = 1325
    competitor_1_ads_or_pens_lower_y = 1385
    competitor_1_ads_or_pens_left_x = 680
    competitor_1_ads_or_pens_right_x = 750

    # Competitor 2 Advantages &/or Penalties
    competitor_2_ads_or_pens_upper_y = 1385
    competitor_2_ads_or_pens_lower_y = 1440
    competitor_2_ads_or_pens_left_x = 690
    competitor_2_ads_or_pens_right_x = 755


