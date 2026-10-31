from pathlib import Path
from typing import Tuple, Optional

import cv2
import numpy as np
from cv2 import Mat


class ReceiptPreprocessor:
    """
    Preprocesare imagini cu bonuri fiscale folosind OpenCV.

    Flux recomandat:
        preprocessor = ReceiptPreprocessor()
        warped, warped_path = preprocessor.process_receipt(
            ReceiptPreprocessor.OperationFactory.WARP,
            "cale/catre/bon.jpeg"
        )

    Observatii:
    - Detectarea bonului se face pe imaginea color, daca este disponibila.
    - Transformarea perspectiva se aplica imaginii originale grayscale,
      nu imaginii binarizate folosite pentru detectie.
    - Padding-ul nu se aplica repetat.
    - Ferestrele OpenCV sunt dezactivate implicit. Pentru debugging:
      ReceiptPreprocessor(show_images=True)
    """

    def __init__(self, show_images: bool = False, save_debug_images: bool = True):
        self.show_images = show_images
        self.save_debug_images = save_debug_images
        self.factory = self.OperationFactory(self)

    @staticmethod
    def extract_source_image_name_and_folder_path(
        image_path: str
    ) -> Tuple[str, str]:
        path = Path(image_path)
        return path.name, str(path.parent)

    @staticmethod
    def _read_image(image_path: str, flags: int = cv2.IMREAD_COLOR) -> Mat:
        image = cv2.imread(str(image_path), flags)
        if image is None:
            raise FileNotFoundError(f"Imaginea nu a putut fi citita: {image_path}")
        return image

    def show_and_write_image(
        self,
        parent_folder_path: str,
        source_image_name: str,
        operation_applied: str,
        image: Mat
    ) -> str:
        """Salveaza rezultatul; il afiseaza numai daca show_images=True."""
        if image is None or image.size == 0:
            raise ValueError(f"Imagine invalida pentru operatia: {operation_applied}")

        output_dir = Path(parent_folder_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        source_stem = Path(source_image_name).stem
        result_image_path = output_dir / f"{source_stem}_{operation_applied}.jpeg"

        success = cv2.imwrite(str(result_image_path), image)
        if not success:
            raise IOError(f"Nu am putut salva imaginea: {result_image_path}")

        if self.show_images:
            cv2.imshow(f"{operation_applied.title()} image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return str(result_image_path)

    def _save_result(self, image_path: str, operation: str, image: Mat) -> str:
        name, folder = self.extract_source_image_name_and_folder_path(image_path)
        return self.show_and_write_image(folder, name, operation, image)

    def process_receipt(
        self,
        operation_applied: str,
        image_path: str
    ) -> Tuple[Mat, str]:
        return self.factory.operation(
            operation_applied=operation_applied,
            image_path=image_path
        )

    def apply_otsu_thresholding(self, image_path: str) -> Tuple[Mat, str]:
        gray = self.factory.grayscale(image_path)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresholded = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
        path = self._save_result(image_path, "otsu_thresholding", thresholded)
        return thresholded, path

    def apply_adaptive_thresholding(self, image_path: str) -> Tuple[Mat, str]:
        gray = self.factory.grayscale(image_path)
        thresholded = self.factory.adaptive_thresholding_from_array(gray)
        path = self._save_result(image_path, "adaptive_thresholding", thresholded)
        return thresholded, path

    def cut_using_thresholding(self, image_path: str) -> Tuple[Mat, str]:
        warped, warped_path = self.factory.operation(
            operation_applied=self.factory.WARP,
            image_path=image_path
        )
        resized, resized_path = self.factory.operation(
            operation_applied=self.factory.RESIZE,
            image_path=warped_path
        )
        return resized, resized_path

    def preprocess_using_thresholding(self, image_path: str) -> Tuple[Mat, str]:
        """
        Corecteaza perspectiva, apoi mareste bonul pentru OCR.
        Returneaza imaginea redimensionata si calea ei.
        """
        return self.cut_using_thresholding(image_path)

    class OperationFactory:
        RESIZE = "resize"
        GRAYSCALE = "grayscale"
        GAUSSIAN_BLUR = "gaussian_blur"
        DYNAMIC_GAUSSIAN_BLUR = "dynamic_gaussian_blur"
        REMOVE_SHADOWS_AND_TEXTURE = "remove_shadows_and_texture"
        OTSU_THRESHOLDING = "otsu_thresholding"
        ADAPTIVE_THRESHOLDING = "adaptive_thresholding"
        WARP = "warp"
        DESKEW = "deskew"

        def __init__(self, outer_instance):
            self.outer = outer_instance

        def operation(
            self,
            operation_applied: str,
            image_path: str
        ) -> Tuple[Mat, str]:
            operations = {
                self.RESIZE: self.resize,
                self.GRAYSCALE: self.grayscale,
                self.GAUSSIAN_BLUR: self.gaussian_blur,
                self.DYNAMIC_GAUSSIAN_BLUR: self.dynamic_gaussian_blur,
                self.REMOVE_SHADOWS_AND_TEXTURE: self.remove_shadows_and_texture,
                self.OTSU_THRESHOLDING: self.otsu_thresholding,
                self.ADAPTIVE_THRESHOLDING: self.adaptive_thresholding,
                self.WARP: self.warp_receipt,
                self.DESKEW: self.deskew,
            }

            if operation_applied not in operations:
                raise ValueError(
                    f"Operatie necunoscuta: {operation_applied}. "
                    f"Operatii disponibile: {', '.join(operations)}"
                )

            result_image = operations[operation_applied](image_path)
            result_path = self.outer._save_result(
                image_path, operation_applied, result_image
            )
            return result_image, result_path

        @staticmethod
        def _read_gray(image_path: str) -> Mat:
            image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                raise FileNotFoundError(f"Imaginea nu a putut fi citita: {image_path}")
            return image

        def resize(self, image_path: str) -> Mat:
            gray = self._read_gray(image_path)
            return cv2.resize(
                gray,
                dsize=None,
                fx=2.5,
                fy=2.5,
                interpolation=cv2.INTER_CUBIC
            )

        def grayscale(self, image_path: str) -> Mat:
            return self._read_gray(image_path)

        def gaussian_blur(self, image_path: str) -> Mat:
            gray = self._read_gray(image_path)
            return cv2.GaussianBlur(gray, (5, 5), 0)

        def dynamic_gaussian_blur(self, image_path: str) -> Mat:
            gray = self._read_gray(image_path)
            h, w = gray.shape[:2]
            kernel_size = max(3, min(int(w * 0.015) | 1, 31))
            return cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

        def remove_shadows_and_texture(self, image_path: str) -> Mat:
            """
            Normalizeaza iluminarea local, apoi reduce textura de fundal.
            Este o operatie optionala; nu este folosita la detectia colturilor.
            """
            gray = self._read_gray(image_path)
            h, w = gray.shape[:2]

            grid = max(4, min(16, int(min(w, h) / 100)))
            clahe = cv2.createCLAHE(
                clipLimit=2.0,
                tileGridSize=(grid, grid)
            )
            normalized = clahe.apply(gray)

            kernel_size = max(15, (int(min(h, w) * 0.04) | 1))
            kernel_size = min(kernel_size, 61)
            background_kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT, (kernel_size, kernel_size)
            )
            background = cv2.morphologyEx(
                normalized, cv2.MORPH_CLOSE, background_kernel
            )
            corrected = cv2.divide(
                normalized, background, scale=255
            )
            return corrected

        def otsu_thresholding(self, image_path: str) -> Mat:
            gray = self._read_gray(image_path)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            return cv2.threshold(
                blurred, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

        @staticmethod
        def adaptive_thresholding_from_array(gray: Mat) -> Mat:
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            h, w = blurred.shape[:2]

            block_size = int(min(w, h) * 0.025)
            block_size = max(11, min(block_size | 1, 99))
            if block_size % 2 == 0:
                block_size += 1

            return cv2.adaptiveThreshold(
                blurred,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                blockSize=block_size,
                C=12
            )

        def adaptive_thresholding(self, image_path: str) -> Mat:
            gray = self._read_gray(image_path)
            return self.adaptive_thresholding_from_array(gray)

        @staticmethod
        def order_points(points: np.ndarray) -> np.ndarray:
            """
            Ordoneaza patru puncte: stanga-sus, dreapta-sus,
            dreapta-jos, stanga-jos.
            """
            points = np.asarray(points, dtype=np.float32).reshape(4, 2)
            ordered = np.zeros((4, 2), dtype=np.float32)

            sums = points.sum(axis=1)
            differences = np.diff(points, axis=1).reshape(-1)

            ordered[0] = points[np.argmin(sums)]       # top-left
            ordered[2] = points[np.argmax(sums)]       # bottom-right
            ordered[1] = points[np.argmin(differences)]  # top-right
            ordered[3] = points[np.argmax(differences)]  # bottom-left
            return ordered

        @staticmethod
        def _candidate_score(contour: np.ndarray, image_shape) -> float:
            h, w = image_shape[:2]
            image_area = float(h * w)
            area = cv2.contourArea(contour)

            if area < image_area * 0.08 or area > image_area * 0.92:
                return -1.0

            x, y, cw, ch = cv2.boundingRect(contour)
            if cw < w * 0.20 or ch < h * 0.20:
                return -1.0

            # Un bon fiscal este de obicei alungit.
            ratio = max(cw, ch) / max(1.0, min(cw, ch))
            if ratio < 1.15 or ratio > 5.5:
                return -1.0

            # Penalizam contururile care ating marginile fotografiei.
            border_penalty = 0.35 if (
                x <= 2 or y <= 2 or x + cw >= w - 2 or y + ch >= h - 2
            ) else 1.0

            return (area / image_area) * border_penalty

        def _find_receipt_contour(self, color_image: Mat) -> np.ndarray:
            """
            Detecteaza conturul bonului.

            Pentru fotografii cu bon alb/albastrui pe masa din lemn,
            separa in primul rand hartia dupa nuanta/saturatie HSV.
            Daca metoda color nu gaseste un candidat, incearca o detectie
            bazata pe muchii si prag adaptiv.
            """
            h, w = color_image.shape[:2]
            hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            # Hartia din fotografia furnizata are o componenta albastru-cyan,
            # in timp ce lemnul are nuante portocalii/maronii si saturatie mare.
            # Intervalul este intentionat suficient de larg pentru variatii
            # de iluminare si balans de alb.
            color_mask = cv2.inRange(
                hsv,
                np.array([85, 20, 90], dtype=np.uint8),
                np.array([130, 165, 255], dtype=np.uint8)
            )

            # Eliminam petele mici, apoi unim zonele apropiate de pe hartie.
            open_kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (5, 5)
            )
            close_kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (17, 17)
            )
            color_mask = cv2.morphologyEx(
                color_mask, cv2.MORPH_OPEN, open_kernel
            )
            color_mask = cv2.morphologyEx(
                color_mask, cv2.MORPH_CLOSE, close_kernel, iterations=2
            )

            contours, _ = cv2.findContours(
                color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            scored = [
                (self._candidate_score(c, (h, w)), c)
                for c in contours
            ]
            scored = [(score, c) for score, c in scored if score > 0]

            if scored:
                return max(scored, key=lambda item: item[0])[1]

            # Fallback: muchii + prag adaptiv. Nu acceptam niciodata automat
            # conturul intregii fotografii.
            gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 9, 60, 60)
            edges = cv2.Canny(gray, 35, 110)

            close_kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT, (7, 7)
            )
            edges = cv2.morphologyEx(
                edges, cv2.MORPH_CLOSE, close_kernel, iterations=2
            )

            adaptive = self.adaptive_thresholding_from_array(gray)
            # Bonul este mai deschis decat masa; combinam muchiile cu
            # componentele luminoase pentru a inchide mai bine conturul.
            light_regions = cv2.threshold(
                gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]
            combined = cv2.bitwise_or(edges, light_regions)
            combined = cv2.morphologyEx(
                combined, cv2.MORPH_CLOSE, close_kernel, iterations=2
            )

            contours, _ = cv2.findContours(
                combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            scored = [
                (self._candidate_score(c, (h, w)), c)
                for c in contours
            ]
            scored = [(score, c) for score, c in scored if score > 0]

            if not scored:
                raise ValueError(
                    "Nu am putut identifica bonul. Verifica fotografia "
                    "sau ajusteaza intervalul HSV din _find_receipt_contour()."
                )

            return max(scored, key=lambda item: item[0])[1]

        def _extract_four_corners(self, contour: np.ndarray) -> np.ndarray:
            """
            Incearca sa obtina un patrulater din contur.
            Daca aproximarea nu are exact 4 puncte, foloseste convex hull
            si minAreaRect ca fallback geometric.
            """
            perimeter = cv2.arcLength(contour, True)

            for epsilon_factor in (0.015, 0.02, 0.025, 0.03, 0.04):
                approx = cv2.approxPolyDP(
                    contour, epsilon_factor * perimeter, True
                )
                if len(approx) == 4 and cv2.isContourConvex(approx):
                    return self.order_points(approx.reshape(4, 2))

            hull = cv2.convexHull(contour)
            rect = cv2.minAreaRect(hull)
            box = cv2.boxPoints(rect)
            return self.order_points(box)

        @staticmethod
        def _perspective_warp(image: Mat, corners: np.ndarray) -> Mat:
            tl, tr, br, bl = corners

            width_top = np.linalg.norm(tr - tl)
            width_bottom = np.linalg.norm(br - bl)
            height_right = np.linalg.norm(br - tr)
            height_left = np.linalg.norm(bl - tl)

            output_width = int(max(width_top, width_bottom))
            output_height = int(max(height_right, height_left))

            if output_width < 20 or output_height < 20:
                raise ValueError("Colturile detectate produc o zona prea mica.")

            # Bonul este portret in mod normal. Nu fortam rotirea daca
            # fotografia contine un bon landscape.
            destination = np.array(
                [
                    [0, 0],
                    [output_width - 1, 0],
                    [output_width - 1, output_height - 1],
                    [0, output_height - 1]
                ],
                dtype=np.float32
            )

            matrix = cv2.getPerspectiveTransform(
                corners.astype(np.float32), destination
            )
            return cv2.warpPerspective(
                image,
                matrix,
                (output_width, output_height),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=255
            )

        def warp_receipt(self, image_path: str) -> Mat:
            """
            Detecteaza bonul in fotografia color si aplica transformarea
            perspective imaginii grayscale originale.

            Important: punctele sunt detectate in coordonatele imaginii
            originale; nu adaugam padding inainte de detectie si nu aplicam
            warp pe imaginea threshold, ci pe imaginea grayscale.
            """
            color_image = self.outer._read_image(
                image_path, cv2.IMREAD_COLOR
            )
            gray_image = cv2.cvtColor(
                color_image, cv2.COLOR_BGR2GRAY
            )

            contour = self._find_receipt_contour(color_image)
            corners = self._extract_four_corners(contour)

            if self.outer.save_debug_images:
                debug = color_image.copy()
                cv2.drawContours(
                    debug, [contour], -1, (0, 255, 0), 4
                )
                for index, (x, y) in enumerate(corners.astype(int)):
                    cv2.circle(debug, (x, y), 12, (0, 0, 255), -1)
                    cv2.putText(
                        debug, str(index + 1), (x + 12, y - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2
                    )
                self.outer._save_result(
                    image_path, "receipt_detection_debug", debug
                )

            warped = self._perspective_warp(gray_image, corners)

            # Imaginea corectata ramane grayscale. Thresholding-ul se poate
            # aplica separat, in functie de cerintele OCR-ului.
            return warped

        def deskew(self, image_path: str) -> Mat:
            gray = self._read_gray(image_path)
            _, binary = cv2.threshold(
                gray, 0, 255,
                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )

            coordinates = np.column_stack(np.where(binary > 0))
            if len(coordinates) < 10:
                return gray

            angle = cv2.minAreaRect(
                coordinates[:, ::-1].astype(np.float32)
            )[-1]

            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            if abs(angle) <= 0.5:
                return gray

            h, w = gray.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(
                center, angle, 1.0
            )

            # Extindem canvas-ul ca sa nu taiem colturile la rotire.
            cos_value = abs(rotation_matrix[0, 0])
            sin_value = abs(rotation_matrix[0, 1])
            new_w = int((h * sin_value) + (w * cos_value))
            new_h = int((h * cos_value) + (w * sin_value))

            rotation_matrix[0, 2] += (new_w / 2) - center[0]
            rotation_matrix[1, 2] += (new_h / 2) - center[1]

            return cv2.warpAffine(
                gray,
                rotation_matrix,
                (new_w, new_h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=255
            )
