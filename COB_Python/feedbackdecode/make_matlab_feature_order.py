from itertools import combinations
import numpy as np


def make_matlab_feature_order(num_channels=32, group_size=4):
    """
    Returns indices that convert:

        [all 32 single-ended features,
         all 496 differential features in itertools.combinations order]

    into the MATLAB EMGChanPairs ordering.
    """

    differential_pairs = list(combinations(range(num_channels), 2))

    # Location of each differential pair in the original 528-vector.
    # The first 32 positions are the single-ended channels.
    pair_to_index = {
        pair: num_channels + pair_index
        for pair_index, pair in enumerate(differential_pairs)
    }

    order = []

    # MATLAB first places each group of four single-ended channels,
    # followed by the six within-group differential pairs.
    for group_start in range(0, num_channels, group_size):
        group = list(
            range(group_start, group_start + group_size)
        )

        # Four single-ended channels
        order.extend(group)

        # Six within-group differential pairs
        for pair in combinations(group, 2):
            order.append(pair_to_index[pair])

    # MATLAB then places all differential pairs between groups.
    for group_start in range(
        0,
        num_channels - group_size,
        group_size
    ):
        current_group = range(
            group_start,
            group_start + group_size
        )

        later_channels = range(
            group_start + group_size,
            num_channels
        )

        for channel_a in current_group:
            for channel_b in later_channels:
                order.append(
                    pair_to_index[(channel_a, channel_b)]
                )

    order = np.asarray(order, dtype=np.int32)

    if order.size != 528:
        raise RuntimeError(
            f"Expected 528 reorder indices, got {order.size}"
        )

    if np.unique(order).size != 528:
        raise RuntimeError(
            "Feature order contains duplicate or missing indices"
        )

    return order