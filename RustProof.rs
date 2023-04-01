
// ----------------------------------------------------------------------
// 
// RustProof.rs
// 
// ----------------------------------------------------------------------


// 
// rustc -O RustProof.rs
// RustProof.exe
// 


use std::time::{Instant, Duration};

// loop to verify 12 is of density 1/2
fn calc_verify_01() {
    let now: Instant = Instant::now();
    let ary: [i64;2] = [3, 4];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_02(now, icount, iouterloop, &ary);
}
// loop to verify 168 is of density 1/2
fn calc_verify_02() {
    let now: Instant = Instant::now();
    let ary: [i64;3] = [3, 7, 8];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_03(now, icount, iouterloop, &ary);
}
// loop to verify 240 is of density 1/2
fn calc_verify_03() {
    let now: Instant = Instant::now();
    let ary: [i64;3] = [3, 5, 16];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_03(now, icount, iouterloop, &ary);
}
// loop to verify 6,720 is of density 1/2
fn calc_verify_04() {
    let now: Instant = Instant::now();
    let ary: [i64;4] = [3, 7, 10, 32];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_04(now, icount, iouterloop, &ary);
}
// loop to verify 14,880 is of density 1/2
fn calc_verify_05() {
    let now: Instant = Instant::now();
    let ary: [i64;4] = [3, 5, 31, 32];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_04(now, icount, iouterloop, &ary);
}
// loop to verify 65,280 is of density 1/2
fn calc_verify_06() {
    let now: Instant = Instant::now();
    let ary: [i64;4] = [3, 5, 17, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_04(now, icount, iouterloop, &ary);
}
// loop to verify 591,360 is of density 1/2
fn calc_verify_07() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 11, 32, 80];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 591,360 is of density 1/2
fn calc_verify_08() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 11, 40, 64];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 833,280 is of density 1/2
fn calc_verify_09() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 10, 62, 64];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 954,240 is of density 1/2
fn calc_verify_10() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 10, 64, 71];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 1,145,760 is of density 1/2
fn calc_verify_11() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 11, 32, 155];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 2,143,680 is of density 1/2
fn calc_verify_12() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 11, 29, 320];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 2,204,160 is of density 1/2
fn calc_verify_13() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 7, 10, 41, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 3,886,080 is of density 1/2
fn calc_verify_14() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 5, 23, 64, 176];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 6,990,720 is of density 1/2
fn calc_verify_15() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 5, 22, 64, 331];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 17,149,440 is of density 1/2
fn calc_verify_16() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [5, 6, 7, 11, 29, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 39,443,712 is of density 1/2
fn calc_verify_17() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 22, 23, 29, 128];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 61,501,440 is of density 1/2
fn calc_verify_18() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 20, 22, 26, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 66,716,160 is of density 1/2
fn calc_verify_19() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 5, 17, 511, 512];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 68,597,760 is of density 1/2
fn calc_verify_20() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 20, 22, 29, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 89,041,920 is of density 1/2
fn calc_verify_21() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 5, 17, 341, 1024];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 99,939,840 is of density 1/2
fn calc_verify_22() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 52, 64, 130];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 99,939,840 is of density 1/2
fn calc_verify_23() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 64, 65, 104];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 101,122,560 is of density 1/2
fn calc_verify_24() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [5, 6, 9, 11, 14, 19, 128];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 118,272,000 is of density 1/2
fn calc_verify_25() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 50, 64, 160];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 130,099,200 is of density 1/2
fn calc_verify_26() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 55, 64, 176];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 133,425,600 is of density 1/2
fn calc_verify_27() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 38, 95, 160];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 187,031,040 is of density 1/2
fn calc_verify_28() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 49, 56, 64, 71];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 209,932,800 is of density 1/2
fn calc_verify_29() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 50, 71, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 229,152,000 is of density 1/2
fn calc_verify_30() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 50, 64, 310];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 236,651,520 is of density 1/2
fn calc_verify_31() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 71, 124, 128];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 262,416,000 is of density 1/2
fn calc_verify_32() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 50, 64, 355];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 272,912,640 is of density 1/2
fn calc_verify_33() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 71, 128, 143];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 366,213,120 is of density 1/2
fn calc_verify_34() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 52, 131, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 367,933,440 is of density 1/2
fn calc_verify_35() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 59, 116, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 421,048,320 is of density 1/2
fn calc_verify_36() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 40, 89, 512];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 426,961,920 is of density 1/2
fn calc_verify_37() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 32, 152, 380];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 435,240,960 is of density 1/2
fn calc_verify_38() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 46, 128, 352];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 514,631,040 is of density 1/2
fn calc_verify_39() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 32, 236, 295];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 522,762,240 is of density 1/2
fn calc_verify_40() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 10, 44, 221, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 546,712,320 is of density 1/2
fn calc_verify_41() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 32, 172, 430];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 546,712,320 is of density 1/2
fn calc_verify_42() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 32, 215, 344];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 623,293,440 is of density 1/2
fn calc_verify_43() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 34, 155, 512];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 870,481,920 is of density 1/2
fn calc_verify_44() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 112, 128, 176];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 1,045,524,480 is of density 1/2
fn calc_verify_45() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 28, 44, 221, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 1,080,330,240 is of density 1/2
fn calc_verify_46() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 128, 139, 176];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 1,454,046,720 is of density 1/2
fn calc_verify_47() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 5, 17, 259, 22016];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 1,565,921,280 is of density 1/2
fn calc_verify_48() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 112, 128, 331];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 1,733,698,560 is of density 1/2
fn calc_verify_49() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 124, 128, 331];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 1,788,695,040 is of density 1/2
fn calc_verify_50() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 31, 44, 128, 683];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 1,923,018,240 is of density 1/2
fn calc_verify_51() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 103, 221, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,067,394,560 is of density 1/2
fn calc_verify_52() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 76, 256, 308];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,067,394,560 is of density 1/2
fn calc_verify_53() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 77, 256, 304];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,195,128,320 is of density 1/2
fn calc_verify_54() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 512, 640];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,196,606,720 is of density 1/2
fn calc_verify_55() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 77, 256, 323];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,393,825,280 is of density 1/2
fn calc_verify_56() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 64, 308, 352];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,606,714,880 is of density 1/2
fn calc_verify_57() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 608, 640];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,650,306,560 is of density 1/2
fn calc_verify_58() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 64, 341, 352];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,658,163,200 is of density 1/2
fn calc_verify_59() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 620, 640];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,685,281,280 is of density 1/2
fn calc_verify_60() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 88, 128, 691];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,709,611,520 is of density 1/2
fn calc_verify_61() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 632, 640];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,722,473,600 is of density 1/2
fn calc_verify_62() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 635, 640];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 2,915,404,800 is of density 1/2
fn calc_verify_63() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 512, 850];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 3,429,888,000 is of density 1/2
fn calc_verify_64() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 400, 1280];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 3,644,256,000 is of density 1/2
fn calc_verify_65() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 425, 1280];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 4,294,901,760 is of density 1/2
fn calc_verify_66() {
    let now: Instant = Instant::now();
    let ary: [i64;5] = [3, 5, 17, 257, 65536];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_05(now, icount, iouterloop, &ary);
}
// loop to verify 4,638,036,480 is of density 1/2
fn calc_verify_67() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 64, 341, 616];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 4,665,239,040 is of density 1/2
fn calc_verify_68() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 64, 343, 616];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 4,918,911,360 is of density 1/2
fn calc_verify_69() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 64, 341, 683];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 5,311,299,840 is of density 1/2
fn calc_verify_70() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 64, 308, 781];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 5,379,306,240 is of density 1/2
fn calc_verify_71() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 64, 308, 791];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 6,259,545,600 is of density 1/2
fn calc_verify_72() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 7, 11, 29, 365, 2560];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 7,608,944,640 is of density 1/2
fn calc_verify_73() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 89, 121, 2048];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 9,835,668,480 is of density 1/2
fn calc_verify_74() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 92, 128, 2531];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 17,012,244,480 is of density 1/2
fn calc_verify_75() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [5, 6, 7, 11, 29, 496, 512];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 22,160,307,840 is of density 1/2
fn calc_verify_76() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 64, 187, 5611];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 42,365,266,944 is of density 1/2
fn calc_verify_77() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 22, 23, 26, 256, 599];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 46,646,476,800 is of density 1/2
fn calc_verify_78() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 58, 85, 160, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 50,651,166,720 is of density 1/2
fn calc_verify_79() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 5, 46, 56, 64, 133, 154];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 51,140,812,800 is of density 1/2
fn calc_verify_80() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 47, 128, 160, 230];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 52,276,224,000 is of density 1/2
fn calc_verify_81() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 100, 221, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 53,490,877,440 is of density 1/2
fn calc_verify_82() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 5, 49, 56, 71, 128, 143];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 54,042,985,920 is of density 1/2
fn calc_verify_83() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 77, 133, 15296];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 56,220,003,840 is of density 1/2
fn calc_verify_84() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 22, 71, 256, 9373];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 56,888,832,000 is of density 1/2
fn calc_verify_85() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 50, 104, 185, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 62,125,916,160 is of density 1/2
fn calc_verify_86() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 5, 44, 49, 112, 128, 134];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 63,926,016,000 is of density 1/2
fn calc_verify_87() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 47, 128, 200, 230];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 63,961,497,600 is of density 1/2
fn calc_verify_88() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 104, 256, 260];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 63,961,497,600 is of density 1/2
fn calc_verify_89() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 130, 208, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 65,079,168,000 is of density 1/2
fn calc_verify_90() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 50, 124, 128, 355];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 65,079,168,000 is of density 1/2
fn calc_verify_91() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 62, 71, 250, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 68,313,907,200 is of density 1/2
fn calc_verify_92() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 38, 95, 256, 320];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 68,313,907,200 is of density 1/2
fn calc_verify_93() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 128, 152, 380];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 68,313,907,200 is of density 1/2
fn calc_verify_94() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 128, 190, 304];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 71,597,137,920 is of density 1/2
fn calc_verify_95() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 5, 46, 47, 112, 128, 154];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 72,156,564,480 is of density 1/2
fn calc_verify_96() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 52, 95, 128, 494];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 74,970,255,360 is of density 1/2
fn calc_verify_97() {
    let now: Instant = Instant::now();
    let ary: [i64;6] = [3, 5, 23, 53, 1456, 2816];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_06(now, icount, iouterloop, &ary);
}
// loop to verify 75,031,756,800 is of density 1/2
fn calc_verify_98() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 130, 244, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 79,242,240,000 is of density 1/2
fn calc_verify_99() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 128, 250, 268];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 79,268,259,840 is of density 1/2
fn calc_verify_100() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 47, 128, 155, 368];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 79,573,401,600 is of density 1/2
fn calc_verify_101() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 116, 256, 290];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
// loop to verify 79,573,401,600 is of density 1/2
fn calc_verify_102() {
    let now: Instant = Instant::now();
    let ary: [i64;7] = [3, 7, 11, 40, 145, 232, 256];
    let iouterloop: i64 = ary.iter().fold(1i64, |a, &b| a * b) + 1;
    let iinnerloop: usize = ary.len();
    let mut icount: i64 = 0;
    for i in 1..iouterloop {
        for j in 0..iinnerloop {
            if i >= ary[j] && i % ary[j] == 0 {
                icount += 1;
                break;
            }
        }
    }
    print_07(now, icount, iouterloop, &ary);
}
fn print_02(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;2]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
fn print_03(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;3]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
fn print_04(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;4]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
fn print_05(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;5]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
fn print_06(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;6]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
fn print_07(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;7]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
/*
fn print_08(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;8]) {
    let dt: Duration = now.elapsed();
    println!("");
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
fn print_09(now: Instant, icount: i64, iouterloop: i64, ary: &[i64;9]) {
    println!("");
    let dt: Duration = now.elapsed();
    println!("after {} minutes", (dt.as_secs() as f64) / (60.0 as f64)); 
    println!("{:?}", ary);
    println!("{0} / {1}", icount, iouterloop - 1); 
    println!("{}", (icount as f64) / ((iouterloop - 1) as f64));
}
*/

fn main() {
    calc_verify_01();
    calc_verify_02();
    calc_verify_03();
    calc_verify_04();
    calc_verify_05();
    calc_verify_06();
    calc_verify_07();
    calc_verify_08();
    calc_verify_09();
    calc_verify_10();
    calc_verify_11();
    calc_verify_12();
    calc_verify_13();
    calc_verify_14();
    calc_verify_15();
    calc_verify_16();
    calc_verify_17();
    calc_verify_18();
    calc_verify_19();
    calc_verify_20();
    calc_verify_21();
    calc_verify_22();
    calc_verify_23();
    calc_verify_24();
    calc_verify_25();
    calc_verify_26();
    calc_verify_27();
    calc_verify_28();
    calc_verify_29();
    calc_verify_30();
    calc_verify_31();
    calc_verify_32();
    calc_verify_33();
    calc_verify_34();
    calc_verify_35();
    calc_verify_36();
    calc_verify_37();
    calc_verify_38();
    calc_verify_39();
    calc_verify_40();
    calc_verify_41();
    calc_verify_42();
    calc_verify_43();
    calc_verify_44();
    calc_verify_45();
    calc_verify_46();
    calc_verify_47();
    calc_verify_48();
    calc_verify_49();
    calc_verify_50();
    calc_verify_51();
    calc_verify_52();
    calc_verify_53();
    calc_verify_54();
    calc_verify_55();
    calc_verify_56();
    calc_verify_57();
    calc_verify_58();
    calc_verify_59();
    calc_verify_60();
    calc_verify_61();
    calc_verify_62();
    calc_verify_63();
    calc_verify_64();
    calc_verify_65();
    calc_verify_66();
    calc_verify_67();
    calc_verify_68();
    calc_verify_69();
    calc_verify_70();
    calc_verify_71();
    calc_verify_72();
    calc_verify_73();
    calc_verify_74();
    calc_verify_75();
    calc_verify_76();
    calc_verify_77();
    calc_verify_78();
    calc_verify_79();
    calc_verify_80();
    calc_verify_81();
    calc_verify_82();
    calc_verify_83();
    calc_verify_84();
    calc_verify_85();
    calc_verify_86();
    calc_verify_87();
    calc_verify_88();
    calc_verify_89();
    calc_verify_90();
    calc_verify_91();
    calc_verify_92();
    calc_verify_93();
    calc_verify_94();
    calc_verify_95();
    calc_verify_96();
    calc_verify_97();
    calc_verify_98();
    calc_verify_99();
    calc_verify_100();
    calc_verify_101();
    calc_verify_102();
}
