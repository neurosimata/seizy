####-------------------------------- Imports --------------------------- ######
import pytest
import numpy as np
from helper.array_helper import find_szr_idx, merge_close, match_szrs_idx, chunk_array
####------------------------------- Fixtures --------------------------- ######

def create_bin_array(length, index):
    """
    Create binary array based on index.

    Parameters
    ----------
    length : int, array length
    index : 2D list, containing indx[[start1,stop1], [start2,stop2]]

    Returns
    -------
    arr : array, binary
    
    """
    arr = np.zeros(length)
    for i in index:
        arr[i[0]: i[1]+1] = 1
    return arr

@pytest.fixture
def properties():
    prop = {}
    return prop

@pytest.fixture
def create_binary_array():
    return create_bin_array


####--------------------------------------------------- ######


####---------------------------- Tests -------------------------- ######
@pytest.mark.parametrize("length, index", 
                          [(100, [[1, 5], [11, 15]]), 
                           (100, [[0, 4], [30, 60]]),
                           (100, [[1, 2], [15, 20], [90, 99]]),
                          ])
def test_find_szr_index(create_binary_array, length, index):
    
    # create array and find original bounds
    arr = create_binary_array(length, index)
    szr_bounds = find_szr_idx(arr, dur=0)
    assert np.allclose(szr_bounds, np.array(index))


@pytest.mark.parametrize("length, index, dur", 
                          [(100, [[1, 5], [11, 15], [50, 51]], 2),
                           (100, [[1, 1], [11, 15], [50, 51]], 1),
                           (100, [[0, 4], [30, 60]], 5),
                           (100, [[1, 2], [15, 17], [90, 94]], 3),
                          ])
def test_find_szr_index_bounds(create_binary_array, length, index, dur):
    
    # create array and find original bounds
    arr = create_binary_array(length, index)
    szr_bounds = find_szr_idx(arr, dur)
    
    # get seizure duration
    index = np.array(index)
    true_times = index[:,1] - index[:,0] 
    assert szr_bounds.shape[0] == np.sum(true_times >= dur)


@pytest.mark.parametrize("length, index, merge_margin, true_bounds_merged", 
                          [(100, [[1, 5], [11, 15]], 5, [[1, 5], [11, 15]]), 
                           (100, [[1, 5], [11, 15]], 7,  [[1, 15]]),
                           (100, [[0, 5], [20, 30], [31, 50]], 2,  [[0, 5], [20, 50]]),
                           (100, [[1, 2], [10, 20], [90, 99]], 3, [[1, 2], [10, 20], [90, 99]]),
                           (100, [[1, 2], [10, 20], [90, 99]], 9, [[1, 20], [90, 99]]),
                          ])
def test_merge_close(create_binary_array, length, index,
                     merge_margin, true_bounds_merged):
    
    # create array and find original bounds
    arr = create_binary_array(length, index)
    szr_bounds = find_szr_idx(arr, dur=0)
    merged_bounds = merge_close(szr_bounds, merge_margin=merge_margin)
    assert np.allclose(merged_bounds, true_bounds_merged)


@pytest.mark.parametrize("length, index_true, index_pred, matching", 
                          [(100, [[1, 5], [11, 15], [50, 51]], [[4, 4], [12, 14]], 1), 
                           (100, [[0, 4], [30, 60]],  [[4, 5], [12, 14]], 1),
                           (100, [[1, 10], [15, 20], [90, 94]], [[1, 5], [18, 18], [91, 94]], 2),
                          ])
def test_find_szr_match_szrs_idx(create_binary_array, length,
                                 index_true, index_pred, matching):
    
    # get true bounds and pred array
    true_arr = create_binary_array(length, index_true)
    true_bounds = find_szr_idx(true_arr)
    pred_arr = create_binary_array(length, index_pred)
    
    # find matching index
    remove_bounds = np.array([0,1])
    idx = match_szrs_idx(true_bounds, pred_arr, remove_bounds)
    assert idx.sum() == matching


@pytest.mark.parametrize("start, stop, div, true_idx", 
                          [(1, 40, 20, [[1, 20], [21, 40]]), 
                           (1, 41, 20, [[1, 20], [21, 40], [41, 41]]),
                           (1, 52, 20, [[1, 20], [21, 40], [41, 52]]),
                           (5, 52, 20, [[5, 24], [25, 44], [45, 52]]),
                           (5, 64, 20, [[5, 24], [25, 44], [45, 64]]),
                           (5, 65, 20, [[5, 24], [25, 44], [45, 64], [65, 65]]),
                           (1, 39, 13, [[1, 13], [14, 26], [27, 39]]),
                          ])
def test_chunk_array(start, stop, div, true_idx):
 
    idx = chunk_array(start, stop, div)
    assert np.allclose(true_idx, idx)














