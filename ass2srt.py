import re
import sys
import chardet

def replace_ass_n_by_system_n(str_temp):
    return str_temp.replace(r'\N{\rEN}', '\n').replace(r'\N', '\n')


def replace_italic_tags(str_temp):
    return str_temp.replace(r'{\i1}', '<i>').replace(r'{\i0}', '</i>')


def replace_bold_tags(str_temp):
    return str_temp.replace(r'{\b1}', '<b>').replace(r'{\b0}', '</b>')


def remove_b100_to_b900_explicit_bold_weight(str_temp):
    return re.sub(r'{\\b[1-9]00}', '', str_temp)


def replace_underline_tags(str_temp):
    return str_temp.replace(r'{\u1}', '<u>').replace(r'{\u0}', '</u>')


def remove_strikeout_tags(str_temp):
    return re.sub(r'{\\s[0-1]\}', '', str_temp)


def remove_border_tags_and_extended(str_temp):
    return re.sub(r'{\\[x-y]?bord[0-9]*\.?[0-9]*\}', '', str_temp)


def remove_shadow_distance_and_extended(str_temp):
    return re.sub(r'{\\[x-y]?shad[0-9]*\.?[0-9]*\}', '', str_temp)


def remove_blur_edge(str_temp):
    return re.sub(r'{\\be[0-9]*\}', '', str_temp)


def remove_blur_edge_gaussian_kernel(str_temp):
    return re.sub(r'{\\blur[0-9]*\.?[0-9]*\}', '', str_temp)


def remove_font_name(str_temp, fonts_name_list):
    regex_fonts_name = "|".join(fonts_name_list)
    return re.sub(r'{\\fn(' + regex_fonts_name + ')}', '', str_temp)


def remove_font_size(str_temp):
    return re.sub(r'{\\fs[0-9]*\}', '', str_temp)


def remove_font_scale(str_temp):
    return re.sub(r'{\\fsc[x-y]?[0-9]*\}', '', str_temp)


def remove_letter_spacing(str_temp):
    return re.sub(r'{\\fsp-?[0-9]*\.?[0-9]*\}', '', str_temp)


def remove_text_rotation(str_temp):
    return re.sub(r'{\\fr[x-z]?-?[0-9]*\}', '', str_temp)


def remove_text_shearing(str_temp):
    return re.sub(r'{\\fa[x-y]+-?[0-9]*\.?[0-9]*\}', '', str_temp)


def remove_font_encoding(str_temp):
    return re.sub(r'{\\fe[0-9]*\}', '', str_temp)


def replace_text_color(str_temp):
    return re.sub(r'{\\[1-4]?c&H[0-9a-fA-F]{6}&\}', '', str_temp)


def remove_transparency_text_alpha(str_temp):
    return re.sub(r'{\\[1-4]?a(?:lpha)?&H[0-9a-fA-F]{2}&\}', '', str_temp)


def remove_line_alignment(str_temp):
    return re.sub(r'{\\a[n]?[0-9]+\}', '', str_temp)


def remove_karaoke_effect(str_temp):
    return re.sub(r'{\\[k,K][fot]?[0-9]*\}', '', str_temp)


def remove_wrap_style(str_temp):
    return re.sub(r'{\\q[0-3]*\}', '', str_temp)


def remove_reset_style(str_temp, style_list):
    regex_style_names = "|".join(style_list)
    return re.sub(r'{\\r(' + regex_style_names + ')?}', '', str_temp)


def remove_text_position(str_temp):
    return re.sub(r'{\\pos\([0-9]*, ?[0-9]*\)\}', '', str_temp)


def remove_movement(str_temp):
    return re.sub(r'{\\move\([0-9]*, ?[0-9]*, ?[0-9]*, ?[0-9]*,? ?[0-9]*,? ?[0-9]*\)\}', '', str_temp)


def remove_rotation(str_temp):
    return re.sub(r'{\\org\([0-9]*, ?[0-9]*\)\}', '', str_temp)


def remove_fade(str_temp):
    return re.sub(r'{\\fad\([0-9]*, ?[0-9]*,? ?[0-9]*,? ?[0-9]*,? ?[0-9]*,? ?[0-9]*,? ?[0-9]*\)\}', '', str_temp)


def remove_clip_rectangle(str_temp):
    return re.sub(r'{\\[i]?clip\([0-9]*, ?[0-9]*, ?[0-9]*, ?[0-9]*\)\}', '', str_temp)

class Ass2srt:
    def __init__(self, filename):
        self.filename = filename
        # self.load()
        self.fonts_name_list = []
        self.style_list = []

    def output_name(self, tag=None):
        outputfile = self.filename[0:-4]
        if tag:
            outputfile = outputfile+"."+tag
        return outputfile+".srt"

    def load(self, filename=None):
        if filename is None:
            filename = self.filename

        with open(file=filename, mode="r", encoding="utf-8") as f:
            data = f.readlines()

        self.nodes = []
        for line in data:
            if line.startswith("Dialogue"):
                line = line.lstrip("Dialogue:")
                node = line.split(",")
                node[1] = timefmt(node[1])
                node[2] = timefmt(node[2])
                #node[9] = re.sub(r'{.*}', "", node[9]).strip()
                node[9] = re.sub(r'\\N', "\n", node[9])
                self.nodes.append(node)
                # print(f"{node[1]}-->{node[2]}:{node[9]}\n")

    def to_srt(self, name=None, line=0, tag=None):
        if name is None:
            name = self.output_name(tag=tag)
        with open(file=name, mode="w", encoding="utf-8") as f:
            index = 1
            for node in self.nodes:
                f.writelines(f"{index}\n")
                f.writelines(f"{node[1]} --> {node[2]}\n")
                if line == 1:
                    text = node[9].split("\n")[0]
                elif line == 2:
                    tmp = node[9].split("\n")
                    if len(tmp) > 1:
                        text = tmp[1]
                else:
                    text = node[9]
                f.writelines(f"{text}\n\n")
                index += 1
            print(f"字幕转换完成:{self.filename}-->{name}")

    def __str__(self):
        return f"文件名:{self.filename}\n合计{len(self.nodes)}条字幕\n"

    def remove_ass_tags(self, str_input):
        # Remove current \n
        str_temp = str_input.replace('\n', '')
        str_temp = replace_ass_n_by_system_n(str_temp)

        # Source of all ASS Tags: http://docs.aegisub.org/3.2/ASS_Tags/
        str_temp = replace_italic_tags(str_temp)
        str_temp = replace_bold_tags(str_temp)
        str_temp = remove_b100_to_b900_explicit_bold_weight(str_temp)
        str_temp = replace_underline_tags(str_temp)
        str_temp = remove_strikeout_tags(str_temp)
        str_temp = remove_border_tags_and_extended(str_temp)
        str_temp = remove_shadow_distance_and_extended(str_temp)
        str_temp = remove_blur_edge_gaussian_kernel(str_temp)
        str_temp = remove_font_name(str_temp, self.fonts_name_list)
        str_temp = remove_font_size(str_temp)
        str_temp = remove_font_scale(str_temp)
        str_temp = remove_letter_spacing(str_temp)
        str_temp = remove_text_rotation(str_temp)
        str_temp = remove_text_shearing(str_temp)
        str_temp = remove_font_encoding(str_temp)
        str_temp = replace_text_color(str_temp)
        str_temp = remove_transparency_text_alpha(str_temp)
        str_temp = remove_line_alignment(str_temp)
        str_temp = remove_karaoke_effect(str_temp)
        str_temp = remove_wrap_style(str_temp)
        str_temp = remove_reset_style(str_temp, self.style_list)
        str_temp = remove_text_position(str_temp)
        str_temp = remove_movement(str_temp)
        str_temp = remove_rotation(str_temp)
        str_temp = remove_fade(str_temp)
        str_temp = remove_clip_rectangle(str_temp)

        # Add \n at the end of the line
        str_temp += '\n\n'
        return str_temp

    def convert_ass_to_srt(self, srt_filename=None, line=0, tag=None):
        if srt_filename is None:
            srt_filename = self.output_name(tag=tag)
        output_srt_file = srt_filename
        ass_filename = self.filename
        if ass_filename.lower().endswith('.ass'):
            try:
                with open(ass_filename, 'rb') as ass_opened_file:
                    char_enc = chardet.detect(ass_opened_file.read())['encoding']
                with open(ass_filename, 'r', encoding=char_enc) as infile, open(output_srt_file, 'w', encoding=char_enc) as outfile:
                    # I'm doing a loop over each lines, event_line is used to know if we have reach the [Events] section
                    event_line = False
                    dialogue_number = 1  # the number indicating which subtitle it is in the sequence.
                    for line in infile:
                        if not event_line:
                            """
                            Removes the [Script Info] and [V4+ Styles] headers
                            + The Format line on the [Events] section
                            """
                            if line.startswith("Style: "):
                                split_line = line.split(",")
                                style_name = split_line[0]
                                if style_name not in self.style_list:
                                    self.style_list.append(style_name)
                                font_name = split_line[1]
                                if font_name not in self.fonts_name_list:
                                    self.fonts_name_list.append(font_name)
                            if line.startswith("Format: Layer"):
                                event_line = True
                        else:
                            """
                            We are now on the Dialogue lines
                            """
                            if line not in ['\n', '\r\n'] or len(line.strip()) != 0:
                                outfile.write(str(dialogue_number) + '\n')
                                tmp_line = line.split(",", 9)
                                outfile.write(tmp_line[1].replace(".", ",") + " --> " + tmp_line[2].replace(".", ",") + '\n')
                                outfile.write(self.remove_ass_tags(tmp_line[9]))
                                dialogue_number += 1
                outfile.close()
                infile.close()
            except EnvironmentError:
                print("The file " + ass_filename + " does not exist")
                exit(10)

def timefmt(strt):
    strt = strt.replace(".", ",")
    return f"{strt}0"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help=".ass file to convert")
    parser.add_argument("-s", "--suffix", default="zh", choices=["zh", "en", "fr", "de"],
                        help="add suffix to subtitles name")
    parser.add_argument("-l", "--line", type=int,
                        choices=[0, 1, 2], default=0, help="keep double subtitles")
    parser.add_argument("-i", "--info", action="store_true",
                        help="display subtitles infomation")
    parser.add_argument("-o", "--out", help="output file name")

    args = parser.parse_args()

    if args.file is None:
        parser.print_help()

    app = Ass2srt(args.file)
    if args.info:
        print(app)
        sys.exit()

    line = 0
    if args.line:
        line = args.line

    #app.to_srt(name=args.out, line=line, tag=args.suffix)
    app.convert_ass_to_srt(srt_filename=args.out, line=line, tag=args.suffix)


if __name__ == "__main__":
    main()
