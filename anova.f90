!gfortran -g -O0 -fbacktrace -ggdb -fcheck=bounds,do,mem,pointer -ffpe-trap=invalid,zero,overflow -ffree-line-length-none anova.f90
MODULE support
   INTEGER                                           :: nf
   INTEGER          , DIMENSION(:)     , ALLOCATABLE :: nl
   INTEGER                                           :: mcell
   INTEGER                                           :: nl_max
   INTEGER                                           :: num_partitions
   INTEGER          , DIMENSION(10)                  :: lev_index

   CHARACTER(LEN=80), DIMENSION(:)     , ALLOCATABLE :: factors
   CHARACTER(LEN=80), DIMENSION(:,:)   , ALLOCATABLE :: levels

   REAL             , DIMENSION(:,:)   , ALLOCATABLE :: y

CONTAINS

   SUBROUTINE get_factors_and_levels
      IMPLICIT NONE
      INTEGER :: fac_loop, lev_loop
      WRITE (*,*) 'How many factors?'
      READ (*,*) nf

      ALLOCATE(factors(nf))
      DO fac_loop = 1 , nf
         WRITE (*,*) 'What is the name of factor #',fac_loop
         READ (*,FMT='(A)') factors(fac_loop)
      END DO
      WRITE (*,*)

      ALLOCATE(nl(nf))
      DO fac_loop = 1 , nf
         WRITE (*,*) 'How many levels for factor ',TRIM(factors(fac_loop))
         READ (*,*) nl(fac_loop)
      END DO
      WRITE (*,*)

      nl_max = MAXVAL(nl)
      ALLOCATE(levels(nl_max,nf))
      DO fac_loop = 1 , nf
         WRITE (*,*) 'For factor ',TRIM(factors(fac_loop))
         DO lev_loop = 1 , nl(fac_loop)
            WRITE (*,*) 'What is the name of level #',lev_loop
            READ (*,FMT='(A)') levels(lev_loop,fac_loop)
         END DO
      END DO
      WRITE (*,*)

      WRITE (*,*) 'Within each cell, how many measurements are taken?'
      READ (*,*) mcell

   END SUBROUTINE get_factors_and_levels

!-------------------------------------------------------------------------------

   SUBROUTINE show_factors_and_levels
      IMPLICIT NONE

      INTEGER :: fac_loop, lev_loop

print *,'num factors = ',nf
do fac_loop = 1,nf
print *,'FACTOR: ',fac_loop,': ',trim(factors(fac_loop))
print *,nl(fac_loop),' levels'
do lev_loop = 1,nl(fac_loop)
print *,'LEVEL: ',lev_loop,': ',trim(levels(lev_loop,fac_loop))
end do
print *,' '
end do

      num_partitions = 1
      DO fac_loop = 1,nf
         num_partitions = num_partitions * nl(fac_loop)
      END DO

   END SUBROUTINE show_factors_and_levels

!-------------------------------------------------------------------------------

   SUBROUTINE bulk_to_bins_3 ( part_loop )
      IMPLICIT NONE

      INTEGER , INTENT(IN) :: part_loop
      INTEGER :: part, fac1, fac2, fac3

      lev_index = 0
      part = 0
      DO fac3 = 1 , nl(3)
         DO fac2 = 1 , nl(2)
            DO fac1 = 1 , nl(1)
               part = part + 1
               IF ( part .EQ. part_loop ) THEN
                  lev_index(1) = fac1
                  lev_index(2) = fac2
                  lev_index(3) = fac3
                  RETURN
               END IF
            END DO
         END DO
      END DO

   END SUBROUTINE bulk_to_bins_3

!-------------------------------------------------------------------------------

   SUBROUTINE bins_to_bulk_3 ( f1l, f2l, f3l, part_loop )
      IMPLICIT NONE

      INTEGER , INTENT(IN ) :: f1l, f2l, f3l
      INTEGER , INTENT(OUT) :: part_loop
      INTEGER :: fac1, fac2, fac3

      part_loop = 0
      DO fac3 = 1 , nl(3)
         DO fac2 = 1 , nl(2)
            DO fac1 = 1 , nl(1)
               part_loop = part_loop + 1
               IF ( ( fac1 .EQ. f1l ) .AND. &
                    ( fac2 .EQ. f2l ) .AND. &
                    ( fac3 .EQ. f3l ) ) THEN
                  RETURN
               END IF
            END DO
         END DO
      END DO

   END SUBROUTINE bins_to_bulk_3

!-------------------------------------------------------------------------------

   SUBROUTINE bulk_to_bins_2 ( part_loop )
      IMPLICIT NONE

      INTEGER , INTENT(IN) :: part_loop
      INTEGER :: part, fac1, fac2

      lev_index = 0
      part = 0
         DO fac2 = 1 , nl(2)
            DO fac1 = 1 , nl(1)
               part = part + 1
               IF ( part .EQ. part_loop ) THEN
                  lev_index(1) = fac1
                  lev_index(2) = fac2
                  RETURN
               END IF
            END DO
         END DO

   END SUBROUTINE bulk_to_bins_2

!-------------------------------------------------------------------------------

   SUBROUTINE bins_to_bulk_2 ( f1l, f2l, part_loop )
      IMPLICIT NONE

      INTEGER , INTENT(IN ) :: f1l, f2l
      INTEGER , INTENT(OUT) :: part_loop
      INTEGER :: fac1, fac2

      part_loop = 0
         DO fac2 = 1 , nl(2)
            DO fac1 = 1 , nl(1)
               part_loop = part_loop + 1
               IF ( ( fac1 .EQ. f1l ) .AND. &
                    ( fac2 .EQ. f2l ) ) THEN
                  RETURN
               END IF
            END DO
         END DO

   END SUBROUTINE bins_to_bulk_2

!-------------------------------------------------------------------------------

   SUBROUTINE bulk_to_bins_1 ( part_loop )
      IMPLICIT NONE

      INTEGER , INTENT(IN) :: part_loop
      INTEGER :: part, fac1

      lev_index = 0
      part = 0
            DO fac1 = 1 , nl(1)
               part = part + 1
               IF ( part .EQ. part_loop ) THEN
                  lev_index(1) = fac1
                  RETURN
               END IF
            END DO

   END SUBROUTINE bulk_to_bins_1

!-------------------------------------------------------------------------------

   SUBROUTINE bins_to_bulk_1 ( f1l, part_loop )
      IMPLICIT NONE

      INTEGER , INTENT(IN ) :: f1l
      INTEGER , INTENT(OUT) :: part_loop
      INTEGER :: fac1

      part_loop = 0
            DO fac1 = 1 , nl(1)
               part_loop = part_loop + 1
               IF ( fac1 .EQ. f1l ) THEN
                  RETURN
               END IF
            END DO

   END SUBROUTINE bins_to_bulk_1

!-------------------------------------------------------------------------------

   SUBROUTINE get_the_data
      IMPLICIT NONE

      INTEGER :: fac_loop, m, part_loop

      ALLOCATE (y(mcell,num_partitions))

      WRITE (*,*) ' '
print *,'num_partitions = ',num_partitions
      DO part_loop = 1 , num_partitions
         IF      ( nf .EQ. 3 ) THEN 
            CALL bulk_to_bins_3 ( part_loop )
         ELSE IF ( nf .EQ. 2 ) THEN 
            CALL bulk_to_bins_2 ( part_loop )
         ELSE IF ( nf .EQ. 1 ) THEN 
            CALL bulk_to_bins_1 ( part_loop )
         END IF
         WRITE (*,FMT='(A)') '========================================================='
print *,'part_loop = ',part_loop
         DO fac_loop = 1, nf
print *,'lev_index = ',lev_index(fac_loop)
print *,'levels    = ',TRIM(levels(lev_index(fac_loop),fac_loop))
            WRITE (*,FMT='(A,A,A,A)') 'Factor = ',TRIM(factors(fac_loop)),', Level = ',TRIM(levels(lev_index(fac_loop),fac_loop))
         END DO
         DO m = 1 , mcell
!           WRITE (*,FMT='(A,I3.3,A)',ADVANCE='NO') '      Index = ',m,'   Value = '
            READ (*,*) y(m,part_loop)
         END DO
      END DO

   END SUBROUTINE get_the_data

!-------------------------------------------------------------------------------

   SUBROUTINE show_the_data
      IMPLICIT NONE

      INTEGER :: fac_loop, m, part_loop

      WRITE (*,*) ' '
      DO part_loop = 1 , num_partitions
         IF      ( nf .EQ. 3 ) THEN 
            CALL bulk_to_bins_3 ( part_loop )
         ELSE IF ( nf .EQ. 2 ) THEN 
            CALL bulk_to_bins_2 ( part_loop )
         ELSE IF ( nf .EQ. 1 ) THEN 
            CALL bulk_to_bins_1 ( part_loop )
         END IF
         WRITE (*,FMT='(A)') '========================================================='
         DO fac_loop = 1, nf
            WRITE (*,FMT='(A,A,A,A)') 'Factor = ',TRIM(factors(fac_loop)),', Level = ',TRIM(levels(lev_index(fac_loop),fac_loop))
         END DO
         DO m = 1 , mcell
            WRITE (*,FMT='(A,I3.3,A,F10.5)') '      Index = ',m,'   Value = ', y(m,part_loop)
         END DO
      END DO

   END SUBROUTINE show_the_data

END MODULE support

!===============================================================================

MODULE stats

   USE support

   !  ANOVA terms

   REAL :: df_mean, ss_mean, ms_mean
   REAL :: df_f1  , ss_f1  , ms_f1   , hold_f1
   REAL :: df_f2  , ss_f2  , ms_f2   , hold_f2
   REAL :: df_f3  , ss_f3  , ms_f3   , hold_f3
   REAL :: df_i12 , ss_i12 , ms_i12  , hold_i12
   REAL :: df_i13 , ss_i13 , ms_i13  , hold_i13
   REAL :: df_i23 , ss_i23 , ms_i23  , hold_i23
   REAL :: df_i123, ss_i123, ms_i123 , hold_i123
   REAL :: df_err , ss_err , ms_err

CONTAINS

   SUBROUTINE three_factor_anova

      IMPLICIT NONE

      CALL three_factor_compute_terms
      CALL three_factor_show

   END SUBROUTINE three_factor_anova

!-------------------------------------------------------------------------------

   SUBROUTINE three_factor_compute_terms

      IMPLICIT NONE

      INTEGER :: fac_loop, lev_loop, m, count, num_part
      INTEGER :: fac1, fac2, fac3
      REAL :: sum

      !  Mean

      df_mean = 1
      ss_mean = 0
      count = 0
      DO num_part = 1 , num_partitions
         DO m = 1 , mcell
            count = count + 1
            ss_mean = ss_mean + y(m,num_part)
         END DO
      END DO
      ss_mean = ss_mean**2 / count
      ms_mean = ss_mean   / df_mean
print *,'ss_mean = ',ss_mean
print *,'ms_mean = ',ms_mean


      !  Factor 1

      fac_loop = 1
      df_f1 = nl(fac_loop) - 1
      ss_f1 = 0
      DO fac1 = 1 , nl(1)
         sum = 0
         count = 0
         DO fac3 = 1 , nl(3)
            DO fac2 = 1 , nl(2)
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
         END DO
         ss_f1 = ss_f1 + sum**2
      END DO
      hold_f1 = ss_f1 / count
      ss_f1   = hold_f1 - ss_mean
      ms_f1   = ss_f1 / df_f1

print *,'ss_f1 = ',ss_f1
print *,'ms_f1 = ',ms_f1

      !  Factor 2
!  df_f2  , ss_f2  , ms_f2

      fac_loop = 2
      df_f2 = nl(fac_loop) - 1
      ss_f2 = 0
      DO fac2 = 1 , nl(2)
         sum = 0
         count = 0
         DO fac3 = 1 , nl(3)
            DO fac1 = 1 , nl(1)
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
         END DO
         ss_f2 = ss_f2 + sum**2
      END DO
      hold_f2 = ss_f2 / count
      ss_f2   = hold_f2 - ss_mean
      ms_f2   = ss_f2 / df_f2

print *,'ss_f2 = ',ss_f2
print *,'ms_f2 = ',ms_f2

      !  Factor 3

      fac_loop = 3
      df_f3 = nl(fac_loop) - 1
      ss_f3 = 0
      DO fac3 = 1 , nl(3)
         sum = 0
         count = 0
         DO fac2 = 1 , nl(2)
            DO fac1 = 1 , nl(1)
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
         END DO
         ss_f3 = ss_f3 + sum**2
      END DO
      hold_f3 = ss_f3 / count
      ss_f3   = hold_f3 - ss_mean
      ms_f3   = ss_f3 / df_f3

print *,'ss_f3 = ',ss_f3
print *,'ms_f3 = ',ms_f3

      !  Interaction with Factor 1 and Factor 2

      df_i12 = df_f1 * df_f2
      ss_i12 = 0
      DO fac1 = 1 , nl(1)
         DO fac2 = 1 , nl(2)
         sum = 0
         count = 0
            DO fac3 = 1 , nl(3)
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
            ss_i12 = ss_i12 + sum**2
         END DO
      END DO
      hold_i12 = ss_i12 / count
      ss_i12 = hold_i12 - hold_f1 - hold_f2 + ss_mean
      ms_i12 = ss_i12 / df_i12

print *,'ss_i12 = ',ss_i12
print *,'ms_i12 = ',ms_i12

      !  Interaction with Factor 1 and Factor 3

      df_i13 = df_f1 * df_f3
      ss_i13 = 0
      DO fac1 = 1 , nl(1)
         DO fac3 = 1 , nl(3)
         sum = 0
         count = 0
            DO fac2 = 1 , nl(2)
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
            ss_i13 = ss_i13 + sum**2
         END DO
      END DO
      hold_i13 = ss_i13 / count
      ss_i13 = hold_i13 - hold_f1 - hold_f3 + ss_mean
      ms_i13 = ss_i13 / df_i13

print *,'ss_i13 = ',ss_i13
print *,'ms_i13 = ',ms_i13

      !  Interaction with Factor 2 and Factor 3

      df_i23 = df_f2 * df_f3
      ss_i23 = 0
      DO fac2 = 1 , nl(2)
         DO fac3 = 1 , nl(3)
         sum = 0
         count = 0
            DO fac1 = 1 , nl(1)
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
            ss_i23 = ss_i23 + sum**2
         END DO
      END DO
      hold_i23 = ss_i23 / count
      ss_i23 = hold_i23 - hold_f2 - hold_f3 + ss_mean
      ms_i23 = ss_i23 / df_i23

print *,'ss_i23 = ',ss_i23
print *,'ms_i23 = ',ms_i23

      !  Interaction with Factor 1 and Factor 2 and Factor 3

      df_i123 = df_f1 * df_f2 * df_f3
      ss_i123 = 0
      DO fac1 = 1 , nl(1)
         DO fac2 = 1 , nl(2)
            DO fac3 = 1 , nl(3)
               sum = 0
               count = 0
               CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
               ss_i123 = ss_i123 + sum**2
            END DO
         END DO
      END DO
      hold_i123 = ss_i123 / count
      ss_i123 = hold_i123 - hold_i12 - hold_i13 - hold_i23 + hold_f1 + hold_f2 + hold_f3 - ss_mean
      ms_i123 = ss_i123 / df_i123

print *,'ss_i123 = ',ss_i123
print *,'ms_i123 = ',ms_i123

      !  Error

      df_err = nl(1) * nl(2) * nl(3) * mcell - nl(1) * nl(2) * nl(3)
      ss_err = 0
      DO fac1 = 1 , nl(1)
         DO fac2 = 1 , nl(2)
            DO fac3 = 1 , nl(3)
               DO m = 1 , mcell
                  CALL bins_to_bulk_3 ( fac1, fac2, fac3, num_part )
                  sum = y(m,num_part)
                  ss_err = ss_err + sum**2
               END DO
            END DO
         END DO
      END DO
      ss_err = ss_err - hold_i123
      ms_err = ss_err / df_err

print *,'ss_err = ',ss_err
print *,'ms_err = ',ms_err


   END SUBROUTINE three_factor_compute_terms

!-------------------------------------------------------------------------------

   SUBROUTINE three_factor_show

      IMPLICIT NONE

      WRITE (*,*) 
      WRITE (*,FMT='(A)') '                  Source                   df      SS            MS   F Statistic'
      WRITE (*,FMT='(A)') '=================================================================================='
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  'Mean',        NINT(df_mean),      ss_mean,      ms_mean,      ms_mean/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)),        NINT(df_f1),      ss_f1,      ms_f1,      ms_f1/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(2)),        NINT(df_f2),      ss_f2,      ms_f2,      ms_f2/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(3)),        NINT(df_f3),      ss_f3,      ms_f3,      ms_f3/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)) // ' x ' // TRIM(factors(2)),        NINT(df_i12),      ss_i12,      ms_i12,      ms_i12/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)) // ' x ' // TRIM(factors(3)),        NINT(df_i13),      ss_i13,      ms_i13,      ms_i13/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(2)) // ' x ' // TRIM(factors(3)),        NINT(df_i23),      ss_i23,      ms_i23,      ms_i23/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)) // ' x ' // TRIM(factors(2)) // ' x ' // TRIM(factors(3)),        NINT(df_i123),      ss_i123,      ms_i123,      ms_i123/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5)')  'Error',        NINT(df_err),      ss_err,      ms_err

      WRITE (10,*) ms_f2/ms_err
      WRITE (10,*) NINT(df_f2)
      WRITE (10,*) NINT(df_err)


   END SUBROUTINE three_factor_show

!-------------------------------------------------------------------------------

   SUBROUTINE two_factor_anova

      IMPLICIT NONE

      CALL two_factor_compute_terms
      CALL two_factor_show

   END SUBROUTINE two_factor_anova

!-------------------------------------------------------------------------------

   SUBROUTINE two_factor_compute_terms

      IMPLICIT NONE

      INTEGER :: fac_loop, lev_loop, m, count, num_part
      INTEGER :: fac1, fac2
      REAL :: sum

      !  Mean

      df_mean = 1
      ss_mean = 0
      count = 0
      DO num_part = 1 , num_partitions
         DO m = 1 , mcell
            count = count + 1
            ss_mean = ss_mean + y(m,num_part)
         END DO
      END DO
      ss_mean = ss_mean**2 / count
      ms_mean = ss_mean   / df_mean
print *,'ss_mean = ',ss_mean
print *,'ms_mean = ',ms_mean


      !  Factor 1

      fac_loop = 1
      df_f1 = nl(fac_loop) - 1
      ss_f1 = 0
      DO fac1 = 1 , nl(1)
         sum = 0
         count = 0
            DO fac2 = 1 , nl(2)
               CALL bins_to_bulk_2 ( fac1, fac2, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
         ss_f1 = ss_f1 + sum**2
      END DO
      hold_f1 = ss_f1 / count
      ss_f1   = hold_f1 - ss_mean
      ms_f1   = ss_f1 / df_f1

print *,'ss_f1 = ',ss_f1
print *,'ms_f1 = ',ms_f1

      !  Factor 2
!  df_f2  , ss_f2  , ms_f2

      fac_loop = 2
      df_f2 = nl(fac_loop) - 1
      ss_f2 = 0
      DO fac2 = 1 , nl(2)
         sum = 0
         count = 0
            DO fac1 = 1 , nl(1)
               CALL bins_to_bulk_2 ( fac1, fac2, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            END DO
         ss_f2 = ss_f2 + sum**2
      END DO
      hold_f2 = ss_f2 / count
      ss_f2   = hold_f2 - ss_mean
      ms_f2   = ss_f2 / df_f2

print *,'ss_f2 = ',ss_f2
print *,'ms_f2 = ',ms_f2

      !  Interaction with Factor 1 and Factor 2

      df_i12 = df_f1 * df_f2
      ss_i12 = 0
      DO fac1 = 1 , nl(1)
         DO fac2 = 1 , nl(2)
         sum = 0
         count = 0
               CALL bins_to_bulk_2 ( fac1, fac2, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
            ss_i12 = ss_i12 + sum**2
         END DO
      END DO
      hold_i12 = ss_i12 / count
      ss_i12 = hold_i12 - hold_f1 - hold_f2 + ss_mean
      ms_i12 = ss_i12 / df_i12

print *,'ss_i12 = ',ss_i12
print *,'ms_i12 = ',ms_i12

      !  Error

      df_err = nl(1) * nl(2) * mcell - nl(1) * nl(2)
      ss_err = 0
      DO fac1 = 1 , nl(1)
         DO fac2 = 1 , nl(2)
               DO m = 1 , mcell
                  CALL bins_to_bulk_2 ( fac1, fac2, num_part )
                  sum = y(m,num_part)
                  ss_err = ss_err + sum**2
               END DO
         END DO
      END DO
      ss_err = ss_err - hold_i12
      ms_err = ss_err / df_err

print *,'ss_err = ',ss_err
print *,'ms_err = ',ms_err


   END SUBROUTINE two_factor_compute_terms

!-------------------------------------------------------------------------------

   SUBROUTINE two_factor_show

      IMPLICIT NONE

      WRITE (*,*) 
      WRITE (*,FMT='(A)') '                  Source                   df      SS            MS   F Statistic'
      WRITE (*,FMT='(A)') '=================================================================================='
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  'Mean',        NINT(df_mean),      ss_mean,      ms_mean,      ms_mean/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)),        NINT(df_f1),      ss_f1,      ms_f1,      ms_f1/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(2)),        NINT(df_f2),      ss_f2,      ms_f2,      ms_f2/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)) // ' x ' // TRIM(factors(2)),        NINT(df_i12),      ss_i12,      ms_i12,      ms_i12/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5)')  'Error',        NINT(df_err),      ss_err,      ms_err


   END SUBROUTINE two_factor_show

!-------------------------------------------------------------------------------

   SUBROUTINE one_factor_anova

      IMPLICIT NONE

      CALL one_factor_compute_terms
      CALL one_factor_show

   END SUBROUTINE one_factor_anova

!-------------------------------------------------------------------------------

   SUBROUTINE one_factor_compute_terms

      IMPLICIT NONE

      INTEGER :: fac_loop, lev_loop, m, count, num_part
      INTEGER :: fac1
      REAL :: sum

      !  Mean

      df_mean = 1
      ss_mean = 0
      count = 0
      DO num_part = 1 , num_partitions
         DO m = 1 , mcell
            count = count + 1
            ss_mean = ss_mean + y(m,num_part)
         END DO
      END DO
print *,'T..   = ',ss_mean
print *,'T..^2 = ',ss_mean**2
      ss_mean = ss_mean**2 / count
      ms_mean = ss_mean   / df_mean
print *,'ss_mean = ',ss_mean
print *,'ms_mean = ',ms_mean


      !  Factor 1

      fac_loop = 1
      df_f1 = nl(fac_loop) - 1
      ss_f1 = 0
      DO fac1 = 1 , nl(1)
         sum = 0
         count = 0
               CALL bins_to_bulk_1 ( fac1, num_part )
               DO m = 1 , mcell
                  sum = sum + y(m,num_part)
                  count = count + 1
               END DO
print *,'T.j = ',sum, 'T.j^2 = ',sum**2
         ss_f1 = ss_f1 + sum**2
      END DO
      hold_f1 = ss_f1 / count
      ss_f1   = hold_f1 - ss_mean
      ms_f1   = ss_f1 / df_f1

print *,'ss_f1 = ',ss_f1
print *,'ms_f1 = ',ms_f1

      !  Error

      df_err = nl(1) * mcell - nl(1) 
      ss_err = 0
      DO fac1 = 1 , nl(1)
               DO m = 1 , mcell
                  CALL bins_to_bulk_1 ( fac1, num_part )
                  sum = y(m,num_part)
                  ss_err = ss_err + sum**2
               END DO
      END DO
      ss_err = ss_err - hold_f1
      ms_err = ss_err / df_err

print *,'ss_err = ',ss_err
print *,'ms_err = ',ms_err


   END SUBROUTINE one_factor_compute_terms

!-------------------------------------------------------------------------------

   SUBROUTINE one_factor_show

      IMPLICIT NONE

      WRITE (*,*) 
      WRITE (*,FMT='(A)') '                  Source                   df      SS            MS   F Statistic'
      WRITE (*,FMT='(A)') '=================================================================================='
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  'Mean',        NINT(df_mean),      ss_mean,      ms_mean,      ms_mean/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5,F10.3)')  TRIM(factors(1)),        NINT(df_f1),      ss_f1,      ms_f1,      ms_f1/ms_err
      WRITE (*,FMT='(A37,4x,I4.4,2F12.5)')  'Error',        NINT(df_err),      ss_err,      ms_err


   END SUBROUTINE one_factor_show

END MODULE stats

!===============================================================================

PROGRAM computes

   USE support
   USE stats

   IMPLICIT NONE

   INTEGER :: fac_loop, lev_loop

   !  Set up

   CALL get_factors_and_levels
   CALL show_factors_and_levels
   CALL get_the_data
   CALL show_the_data

   !  Analysis

   IF      ( nf .EQ. 3 ) THEN
      CALL three_factor_anova
   ELSE IF ( nf .EQ. 2 ) THEN
      CALL   two_factor_anova
   ELSE IF ( nf .EQ. 1 ) THEN
      CALL   one_factor_anova
   END IF

END PROGRAM computes
