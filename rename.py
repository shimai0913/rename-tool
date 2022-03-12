import os
import re
import argparse

# ========================================================================== #
#  関数名: check_args
# -------------------------------------------------------------------------- #
#  説明: コマンドライン引数の受け取り
#  返り値: dict
# ========================================================================== #
def check_args():
  # ---------------------
  # コマンドライン引数の受け取り
  # ---------------------
  parser = argparse.ArgumentParser(add_help=False)

  # 引数の追加
  parser.add_argument('-dir', help='directory path', required=True)
  parser.add_argument('-filename', help='filename template', required=True)
  # parser.add_argument('--debug', action='store_true')
  args = parser.parse_args()

  try:
    result = {}
    result['dir'] = args.dir
    result['filename'] = args.filename
    # result['debug'] = args.debug
    result['error_code'] = 1

    return result
  except Exception as e:
    # if args.debug:
    print(f'引数指定に誤りがありそうです{e}')
    return 1

# -------------------------------------------------------------------------- #
#  クラス名     MyTool
#  説明        ファイル名変更クラス
#  引数1       dict(コマンドライン引数)
# -------------------------------------------------------------------------- #
class MyTool:
  # [Dont Touch] インスタンス変数
  def __init__(self, args):
    self.def_name = 'init'
    self.target_dir_path = args['dir']
    self.filename_template = args['filename']

    # self.debugflag = args['debug']
    self._error_code = args['error_code']

  # ====================================================================== #
  #  関数名: printLog
  # ---------------------------------------------------------------------- #
  #  説明: ログ
  # ====================================================================== #
  def printLog(self, level, message):
    # with open(r'self.log_path', 'a') as f:
    #     f.write(f'[{level}] {message}\n')
    # if self.debugflag:
    print(f'[{level}] {message}')

  # ========================================================================== #
  #  関数名: countfiles
  # -------------------------------------------------------------------------- #
  #  説明: fileをリスト化
  # ========================================================================== #
  def countfiles(self):
    self.def_name = 'countfiles'
    description = f'Processing of "{self.def_name}" function is started.'
    self.printLog('INFO', f'[ OK ] {description}')

    # メインコード
    # フォルダ内の全ファイル名をリスト化
    files = os.listdir(self.target_dir_path)
    # リストの長さ（ファイル数）を取得
    count = len(files)
    # ファイル数を確認
    self.printLog('INFO', f'"{count}" files found.')

    # ログ作業後処理
    message = f'countfiles completed.'
    self.printLog('INFO', f'[ OK ] {message}')

    return files

  # ========================================================================== #
  #  関数名: rename
  # -------------------------------------------------------------------------- #
  #  説明: fileをrename
  # ========================================================================== #
  def rename(self, file, flag=True):
    self.def_name = 'rename'
    description = f'Processing of "{self.def_name}" function is started.'
    self.printLog('INFO', f'[ OK ] {description}')

    # メインコード
    old_path = self.target_dir_path + file
    root, extension = os.path.splitext(old_path)

    # 変換後のファイル名整形
    num = re.sub(r"\D", "", file)
    file_name = self.filename_template.replace('@', num)
    new_path = self.target_dir_path + file_name + extension

    # ファイル名の変更
    if flag:
      os.rename(old_path, new_path)

    # ログ作業後処理
    message = f'renamed completed. to "{new_path}"'  if flag else f'"{file}" to "{file_name + extension}"'
    self.printLog('INFO', f'[ OK ] {message}')

# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
  # コマンドライン引数の受け取り
  args = check_args()
  assert args != 1, 'Abnormality in argument.'

  tool = MyTool(args)

  files = tool.countfiles()

  for f in files:
    if 'One_Piece_v' in f:
      tool.rename(f, False)

  # 変換後のファイル名に問題がないか確認
  val = input("Is there a problem with the renamed file name? [Y/N]: ")
  if val in ['y', 'Y']:
    for f in files:
      if 'One_Piece_v' in f:
        tool.rename(f)

if __name__ == '__main__':
  main()
