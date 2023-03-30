SPRITE LAYERING Refernce
-----------------------------------


              .---------------Visible Area---------------.
              |                               .----------------------.
              |                               |  <- Upper Eyelid ->  |
              |                                ----------------------
 .----------------------.                                |
 |  <- Lower Eyelid ->  |                                |
  ----------------------                                 |
              |        .-----------------------.         |
              |        |         Pupil <^>     |         |
              v         -----------------------         v
              .------------------------------------------.
              |             Background Color             |
               ------------------------------------------

                       Side view of bitmap layers




EYELID OFFSET REFERENCE
-----------------------------------


    .---------------.
    | Top Eyelid    |
    |               |
  .-|               |-.
  | | ***********   | |1 -\              
  | | **         *  | |2   3 pixel offset    |
  | | *           * | |3 -/                  |
  | '---------------' |4                     v
  |                   |5       Increasing the offset brings
  | .---------------. |6       the eyelids closer together 
  | | *           * | |7                     ^
  | |  *         *  | |8                     |
  | |   *********   | |9                     |
  '-|               |-' 
    |               |
    | Bottom Eyelid |
    '---------------'

                 Top-down view of eyelid layers